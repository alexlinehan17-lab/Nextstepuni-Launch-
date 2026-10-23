#!/usr/bin/env ruby
# frozen_string_literal: true
#
# Adds the study timer's Live Activity to ios/App/App.xcodeproj, scripted so the
# project change can be reviewed and re-run instead of clicked through Xcode:
#
#   - the StudyTimerWidget app extension target (WidgetKit + SwiftUI), bundle id
#     com.nextstepuni.app.StudyTimer, signed the same way as the app (automatic,
#     same team), same version and build numbers, same deployment target;
#   - Shared/StudyTimerAttributes.swift compiled into BOTH targets;
#   - the app's NextStepBridgeViewController.swift and StudyLiveActivityPlugin.swift;
#   - ActivityKit weak-linked, so the app still launches on iOS 15;
#   - the extension embedded in the app (Embed Foundation Extensions).
#
# It provisions nothing. Idempotent: a second run changes nothing.
#
#   gem install --user-install xcodeproj
#   GEM_HOME="$HOME/.gem/ruby/$(ruby -e 'print RbConfig::CONFIG["ruby_version"]')" \
#     ruby scripts/ios/add-study-timer-widget.rb
#
# SPDX-License-Identifier: Apache-2.0

require 'xcodeproj'

ROOT = File.expand_path('../..', __dir__)
PROJECT_PATH = File.join(ROOT, 'ios/App/App.xcodeproj')
WIDGET = 'StudyTimerWidget'
WIDGET_BUNDLE_ID = 'com.nextstepuni.app.StudyTimer'

project = Xcodeproj::Project.open(PROJECT_PATH)
app = project.targets.find { |target| target.name == 'App' } or abort('No App target')

if project.targets.any? { |target| target.name == WIDGET }
  puts "#{WIDGET} is already in the project; nothing to do."
  exit 0
end

# Group references: path relative to the parent group (ios/App/...).
def file_in(group, path)
  group.files.find { |ref| ref.path == path } || group.new_reference(path)
end

app_group = project.main_group.children.find { |child| child.display_name == 'App' } or abort('No App group')
shared_group = project.main_group.new_group('Shared', 'Shared')
widget_group = project.main_group.new_group(WIDGET, WIDGET)

attributes = file_in(shared_group, 'StudyTimerAttributes.swift')
bridge = file_in(app_group, 'NextStepBridgeViewController.swift')
plugin = file_in(app_group, 'StudyLiveActivityPlugin.swift')
widget_bundle = file_in(widget_group, 'StudyTimerWidgetBundle.swift')
live_activity = file_in(widget_group, 'StudyTimerLiveActivity.swift')
assets = file_in(widget_group, 'Assets.xcassets')
file_in(widget_group, 'Info.plist') # read through INFOPLIST_FILE, not copied

app.add_file_references([bridge, plugin, attributes])

# System frameworks resolve against whichever SDK is building (one shared
# SDKROOT reference each, as Xcode makes them).
def link(project, target, framework, weak: false)
  path = "System/Library/Frameworks/#{framework}.framework"
  group = project.frameworks_group['iOS'] || project.frameworks_group.new_group('iOS')
  ref = group.files.find { |file| file.path == path } || group.new_reference(path, :sdk_root)
  build_file = target.frameworks_build_phase.add_file_reference(ref, true)
  build_file.settings = { 'ATTRIBUTES' => ['Weak'] } if weak
end

# The extension, with the app's own signing and version settings.
app_settings = ->(config_name, key) { app.build_configurations.find { |c| c.name == config_name }.build_settings[key] }
widget = project.new_target(:app_extension, WIDGET, :ios, app_settings.call('Release', 'IPHONEOS_DEPLOYMENT_TARGET'),
                            project.products_group, :swift)
# The template links Foundation explicitly; Swift links it anyway.
widget.frameworks_build_phase.files.dup.each do |file|
  ref = file.file_ref
  widget.frameworks_build_phase.remove_build_file(file)
  ref.remove_from_project if ref.build_files.empty?
end
widget.build_configurations.each do |config|
  settings = config.build_settings
  name = config.name
  settings.delete('CLANG_ENABLE_OBJC_WEAK')
  settings['PRODUCT_NAME'] = '$(TARGET_NAME)'
  settings['PRODUCT_BUNDLE_IDENTIFIER'] = WIDGET_BUNDLE_ID
  settings['INFOPLIST_FILE'] = "#{WIDGET}/Info.plist"
  settings['GENERATE_INFOPLIST_FILE'] = 'NO'
  settings['MARKETING_VERSION'] = app_settings.call(name, 'MARKETING_VERSION')
  settings['CURRENT_PROJECT_VERSION'] = app_settings.call(name, 'CURRENT_PROJECT_VERSION')
  settings['DEVELOPMENT_TEAM'] = app_settings.call(name, 'DEVELOPMENT_TEAM')
  settings['CODE_SIGN_STYLE'] = app_settings.call(name, 'CODE_SIGN_STYLE')
  settings['IPHONEOS_DEPLOYMENT_TARGET'] = app_settings.call(name, 'IPHONEOS_DEPLOYMENT_TARGET')
  settings['TARGETED_DEVICE_FAMILY'] = app_settings.call(name, 'TARGETED_DEVICE_FAMILY')
  settings['SWIFT_VERSION'] = app_settings.call(name, 'SWIFT_VERSION')
  settings['SWIFT_ACTIVE_COMPILATION_CONDITIONS'] = name == 'Debug' ? 'DEBUG' : ''
  settings['APPLICATION_EXTENSION_API_ONLY'] = 'YES'
  settings['SKIP_INSTALL'] = 'YES'
  settings['LD_RUNPATH_SEARCH_PATHS'] = ['$(inherited)', '@executable_path/Frameworks', '@executable_path/../../Frameworks']
end

widget.add_file_references([widget_bundle, live_activity, attributes])
widget.add_resources([assets])
link(project, widget, 'WidgetKit')
link(project, widget, 'SwiftUI')
# ActivityKit is iOS 16.1+; the app and extension also run on iOS 15.
link(project, widget, 'ActivityKit', weak: true)
link(project, app, 'ActivityKit', weak: true)

# Build the extension with the app and embed it.
app.add_dependency(widget)
embed = app.new_copy_files_build_phase('Embed Foundation Extensions')
embed.symbol_dst_subfolder_spec = :plug_ins
embed.add_file_reference(widget.product_reference, true).settings = { 'ATTRIBUTES' => ['RemoveHeadersOnCopy'] }

project.root_object.attributes['TargetAttributes'][widget.uuid] = {
  'CreatedOnToolsVersion' => '26.3',
  'ProvisioningStyle' => 'Automatic',
}

project.save
puts "Added #{WIDGET} (#{WIDGET_BUNDLE_ID}) to #{PROJECT_PATH}"

#!/usr/bin/env ruby
# frozen_string_literal: true
# Adds the Screen Time monitor and shared sources. Idempotent; provisions nothing.
require 'xcodeproj'

root = File.expand_path('../..', __dir__)
project = Xcodeproj::Project.open(File.join(root, 'ios/App/App.xcodeproj'))
app = project.targets.find { |target| target.name == 'App' } or abort('No App target')
def group_in(project, name)
  project.main_group.children.find { |g| g.display_name == name } || project.main_group.new_group(name, name)
end
def source_in(group, target, path)
  ref = group.files.find { |f| f.path == path } || group.new_reference(path)
  target.source_build_phase.add_file_reference(ref, true)
end
def link(project, target, framework)
  group = project.frameworks_group['iOS'] || project.frameworks_group.new_group('iOS')
  path = "System/Library/Frameworks/#{framework}.framework"
  ref = group.files.find { |f| f.path == path } || group.new_reference(path, :sdk_root)
  target.frameworks_build_phase.add_file_reference(ref, true)
end

name = 'StudyFocusMonitor'
monitor = project.targets.find { |t| t.name == name } || project.new_target(:app_extension, name, :ios, '16.0', project.products_group, :swift)
monitor.build_configurations.each do |config|
  original = app.build_configurations.find { |c| c.name == config.name }.build_settings
  %w[MARKETING_VERSION CURRENT_PROJECT_VERSION DEVELOPMENT_TEAM CODE_SIGN_STYLE TARGETED_DEVICE_FAMILY SWIFT_VERSION].each do |key|
    config.build_settings[key] = original[key]
  end
  config.build_settings.merge!({
    'PRODUCT_NAME' => '$(TARGET_NAME)',
    'PRODUCT_BUNDLE_IDENTIFIER' => 'com.nextstepuni.app.StudyFocusMonitor',
    'INFOPLIST_FILE' => "#{name}/Info.plist",
    'CODE_SIGN_ENTITLEMENTS' => "#{name}/#{name}.entitlements",
    'GENERATE_INFOPLIST_FILE' => 'NO',
    'IPHONEOS_DEPLOYMENT_TARGET' => '16.0',
    'APPLICATION_EXTENSION_API_ONLY' => 'YES',
    'SKIP_INSTALL' => 'YES',
    'SWIFT_ACTIVE_COMPILATION_CONDITIONS' => config.name == 'Debug' ? 'DEBUG' : '',
    'LD_RUNPATH_SEARCH_PATHS' => ['$(inherited)', '@executable_path/Frameworks', '@executable_path/../../Frameworks'],
  })
end
shared = group_in(project, 'Shared')
%w[StudyFocusPolicy.swift StudyFocusStore.swift].each do |file|
  source_in(shared, app, file)
  source_in(shared, monitor, file)
end
source_in(group_in(project, 'App'), app, 'StudyFocusPlugin.swift')
monitor_group = group_in(project, name)
source_in(monitor_group, monitor, 'StudyFocusMonitor.swift')
%W[Info.plist #{name}.entitlements].each do |file|
  monitor_group.new_reference(file) unless monitor_group.files.any? { |f| f.path == file }
end
%w[FamilyControls ManagedSettings DeviceActivity].each do |framework|
  link(project, app, framework)
  link(project, monitor, framework)
end
link(project, app, 'SwiftUI')
app.add_dependency(monitor) unless app.dependencies.any? { |d| d.target == monitor }
embed = app.copy_files_build_phases.find { |p| p.name == 'Embed Foundation Extensions' } || app.new_copy_files_build_phase('Embed Foundation Extensions')
embed.symbol_dst_subfolder_spec = :plug_ins
embed.add_file_reference(monitor.product_reference, true).settings = { 'ATTRIBUTES' => ['RemoveHeadersOnCopy'] }
attributes = project.root_object.attributes['TargetAttributes'] ||= {}
[app, monitor].each do |target|
  attributes[target.uuid] ||= { 'CreatedOnToolsVersion' => '26.3', 'ProvisioningStyle' => 'Automatic' }
  capabilities = attributes[target.uuid]['SystemCapabilities'] ||= {}
  capabilities['com.apple.FamilyControls'] = { 'enabled' => 1 }
  capabilities['com.apple.ApplicationGroups.iOS'] = { 'enabled' => 1 }
end
project.save
puts 'StudyFocusMonitor and app bridge configured (no provisioning changes).'

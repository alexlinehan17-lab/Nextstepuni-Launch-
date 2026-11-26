import { Fragment, useCallback, useEffect, useRef, useState, type ReactNode, type PointerEvent, type CSSProperties } from 'react';
import { LayoutGroup, motion, useReducedMotion } from 'framer-motion';
import {
  SidebarProvider, Sidebar, SidebarHeader, SidebarContent, SidebarFooter,
  SidebarInset, SidebarTrigger, SidebarGroup, SidebarGroupLabel, SidebarGroupContent,
  SidebarMenu, SidebarMenuItem, SidebarMenuButton,
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuGroup,
  DropdownMenuLabel, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuSub,
  DropdownMenuSubTrigger, DropdownMenuSubContent, DropdownMenuRadioGroup, DropdownMenuRadioItem,
  TooltipProvider, useIsMobile, SoundEffects, SidebarResize,
} from '../kobra-navigation-runtime';
import { NavigationIcon, type NavigationIconName } from './NavigationIcon';
import { useNavigation } from '../../contexts/NavigationContext';
import { sidebarItemFor, type SidebarItemId } from '../../utils/places';
import type { SessionUser } from '../../utils/authUtils';
import type { UserSettings } from '../../types';
import Avatar from '../Avatar';
import NotificationBell from '../NotificationBell';
import { toggleNotificationPanel } from '../../utils/notificationPanel';
import { openShortcutsOverlay } from '../ShortcutsOverlay';
import { auth } from '../../firebase';
import './sidebar.css';

interface Props {
  children: ReactNode;
  user: SessionUser;
  settings: UserSettings;
  updateSetting: <K extends keyof UserSettings>(key: K, value: UserSettings[K]) => void;
  onLogout: () => void;
  onOpenSettings: () => void;
  onOpenPassport: () => void;
  onOpenSiteGuide: () => void;
  onOpenFeedback: () => void;
  /** My Direction, or setting a North Star first when there is none. */
  onOpenDirection: () => void;
  onUnreadCountChange: (count: number) => void;
  completedCount: number;
  totalCount: number;
  unreadCount: number;
}

type Item = { id: SidebarItemId; label: string; icon: NavigationIconName; go: () => void; coach?: string };
const afterMenuCloses = (go: () => void) => window.setTimeout(go, 0);
const DEFAULT_WIDTH = 264;
const MIN_WIDTH = 192;
const MAX_WIDTH = 360;
const WIDTH_STORAGE_KEY = 'nextstepuni-sidebar-width';

/** Uses the current purchased Kobra parts. Only the destinations/brand composition are ours. */
export default function NextStepUniSidebar(props: Props) {
  const mobile = useIsMobile();
  const nav = useNavigation();
  const [open, setOpen] = useState(() => {
    const saved = document.cookie.match(/(?:^|; )sidebar_state=(true|false)(?:;|$)/);
    return saved ? saved[1] === 'true' : true;
  });
  const [hover, setHover] = useState<{ x: number; y: number; width: number; height: number } | null>(null);
  const [preferredWidth, setPreferredWidth] = useState(() => {
    try {
      const saved = Number(localStorage.getItem(WIDTH_STORAGE_KEY));
      return saved >= MIN_WIDTH && saved <= MAX_WIDTH ? saved : DEFAULT_WIDTH;
    } catch { return DEFAULT_WIDTH; }
  });
  const [viewportWidth, setViewportWidth] = useState(() => window.innerWidth);
  const [resizing, setResizing] = useState(false);
  const handleResizingChange = useCallback((value: boolean) => {
    setResizing(value);
    setHover(null);
  }, []);
  const maxWidth = Math.max(MIN_WIDTH, Math.min(MAX_WIDTH, viewportWidth - 480));
  const sidebarWidth = Math.min(preferredWidth, maxWidth);
  useEffect(() => {
    const update = () => setViewportWidth(window.innerWidth);
    window.addEventListener('resize', update);
    return () => window.removeEventListener('resize', update);
  }, []);
  useEffect(() => {
    if (resizing) return;
    try { localStorage.setItem(WIDTH_STORAGE_KEY, String(preferredWidth)); } catch { /* Storage may be unavailable. */ }
  }, [preferredWidth, resizing]);
  const content = useRef<HTMLDivElement>(null);
  const accountTrigger = useRef<HTMLButtonElement>(null);
  const updatesTrigger = useRef<HTMLButtonElement>(null);
  const reduced = useReducedMotion();
  const email = auth.currentUser?.uid === props.user.uid ? auth.currentUser.email : null;
  // Sidebar B (agreed 25 Nov 2026): the five places, then Workspace. Ten rows,
  // and nothing scrolls on a 1280 x 800 laptop. What left the list lives under
  // the student's name (Year Plans, Study Passport, Your setup, Insights, My
  // Direction, Account), on Home (Learning paths) or in the Launchpad (War
  // Room, Future Finder); References stays in Help.
  const current = sidebarItemFor(nav.state);
  const groups: { title?: string; items: Item[] }[] = [
    { items: [
      { id: 'home', label: 'Home', icon: 'home', go: nav.navigateToTree },
      { id: 'modules', label: 'Modules', icon: 'modules', go: nav.navigateToModules, coach: 'modules' },
      { id: 'study', label: 'Study session', icon: 'timer', go: nav.navigateToStudySession, coach: 'study' },
      { id: 'progress', label: 'My Progress', icon: 'progress', go: () => nav.navigateToDashboard() },
      { id: 'island', label: 'My Island', icon: 'island', go: nav.navigateToJourney },
    ] },
    { title: 'Workspace', items: [
      { id: 'launchpad', label: 'Launchpad', icon: 'compass', go: () => nav.navigateToInnovationZone(), coach: 'launchpad' },
      { id: 'mark-bank', label: 'Mark Bank', icon: 'marks', go: () => nav.navigateToInnovationZone('mark-bank') },
      { id: 'planner', label: 'Planner', icon: 'planner', go: () => nav.navigateToInnovationZone('planner') },
      { id: 'topic-atlas', label: 'Topic Atlas', icon: 'atlas', go: () => nav.navigateToInnovationZone('topic-atlas') },
      { id: 'paper-trail', label: 'Paper Trail', icon: 'papers', go: () => nav.navigateToInnovationZone('paper-trail') },
    ] },
  ];

  const highlight = (event: PointerEvent<HTMLDivElement>) => {
    const item = (event.target as Element).closest<HTMLElement>('[data-slot="sidebar-menu-item"]');
    if (!item || !content.current) return setHover(null);
    const row = item.getBoundingClientRect();
    const parent = content.current.getBoundingClientRect();
    setHover({ x: row.left - parent.left, y: row.top - parent.top + content.current.scrollTop, width: row.width, height: row.height });
  };

  // Match the bottom bar's 768px breakpoint on every platform, including native
  // iPads and desktop-mode Safari. Device detection must not leave tablets with
  // neither navigation bar. Narrow Split View windows keep the bottom bar.
  if (mobile) return <>{props.children}<div className="hidden"><NotificationBell uid={props.user.uid} onUnreadCountChange={props.onUnreadCountChange} /></div></>;

  const SoundScope = typeof globalThis.AudioContext === 'function' ? SoundEffects : Fragment;
  return <SoundScope><TooltipProvider>
    <SidebarProvider open={open} onOpenChange={setOpen} className="nsu-kobra-nav student-sidebar-shell" data-resizing={resizing || undefined} data-compact={open && sidebarWidth < 224 || undefined} style={{ '--sidebar-width': `${sidebarWidth}px`, '--sidebar-width-icon': '48px', '--navigation-width': open ? `${sidebarWidth}px` : '64px' } as CSSProperties}>
      <Sidebar variant="inset" collapsible="icon" className="nsu-nav-container">
        <SidebarHeader className="nsu-nav-header">
          <div className="nsu-nav-brand-row">
            <button type="button" className="nsu-nav-wordmark" data-sound="select" onClick={nav.navigateToTree} aria-label="NextStepUni home">nextstepuni<span className="nsu-nav-wordmark-stop" aria-hidden="true">.</span></button>
            <SidebarTrigger className="nsu-nav-collapse" data-sound={open ? 'close' : 'open'} aria-label={open ? 'Collapse sidebar' : 'Expand sidebar'} aria-expanded={open} />
          </div>
        </SidebarHeader>
        <LayoutGroup id="nextstepuni-navigation">
          <SidebarContent ref={content} className="nsu-nav-content" onPointerOver={highlight} onPointerLeave={() => setHover(null)} onScroll={() => setHover(null)}>
            {hover && <motion.span aria-hidden="true" className="nsu-nav-hover" initial={false} animate={{ x: hover.x, y: hover.y, width: hover.width, height: hover.height }} transition={{ duration: reduced ? 0 : .15, ease: [.16, 1, .3, 1] }} />}
            <nav aria-label="Main navigation">
              {groups.map(group => <SidebarGroup key={group.title ?? 'places'} className="nsu-nav-group">
                {group.title && <SidebarGroupLabel className="nsu-nav-group-label">{group.title}</SidebarGroupLabel>}
                <SidebarGroupContent><SidebarMenu>
                  {group.items.map(item => {
                    const active = item.id === current;
                    return <SidebarMenuItem key={item.id} className="nsu-nav-item">
                      <SidebarMenuButton isActive={active} className="nsu-nav-button" data-sound="select" aria-label={item.label} aria-current={active ? 'page' : undefined} tooltip={open ? undefined : item.label} data-coach={item.coach} onClick={item.go} render={<motion.button whileTap={reduced ? undefined : 'pressed'} />}>
                        <motion.span variants={{ pressed: { scale: .96 } }} transition={{ duration: .12, ease: [.23, 1, .32, 1] }} className="nsu-nav-symbol"><NavigationIcon name={item.icon} active={active} /></motion.span>
                        <span className="nsu-nav-label">{item.label}</span>
                      </SidebarMenuButton>
                    </SidebarMenuItem>;
                  })}
                </SidebarMenu></SidebarGroupContent>
              </SidebarGroup>)}
            </nav>
          </SidebarContent>
        </LayoutGroup>
        <SidebarFooter className="nsu-nav-footer">
          <button ref={updatesTrigger} type="button" className="nsu-nav-updates" data-notification-toggle
            data-unread={props.unreadCount > 0 || undefined} onClick={toggleNotificationPanel}
            aria-label={props.unreadCount > 0 ? `Open updates, ${props.unreadCount} unread` : 'Open updates'}
            title={props.unreadCount > 0 ? `${props.unreadCount} unread updates` : 'Updates'}>
            <NavigationIcon name="bell" />
            <span className="nsu-nav-updates-label">Updates</span>
            {props.unreadCount > 0 && <span className="nsu-nav-updates-count">{props.unreadCount > 99 ? '99+' : props.unreadCount}<span className="nsu-nav-updates-new"> new</span></span>}
          </button>
          <DropdownMenu>
            <DropdownMenuTrigger ref={accountTrigger} className="nsu-nav-account" aria-label="Open account menu" data-coach="help">
              <Avatar seed={props.settings.avatar || props.user.avatar} alt="" className="nsu-nav-avatar" />
              <span className="nsu-nav-account-copy"><span>{props.user.name}</span><small>{props.user.isAdmin ? 'Admin' : 'Student'}</small></span>
              <NavigationIcon name="updown" size={16} className="nsu-nav-account-chevron" />
            </DropdownMenuTrigger>
            {/* The menu under the student's name opens beside it, so the list
                above stays in view. It holds what the phone keeps in its
                account sheet: Year Plans, Study Passport, Your setup, and
                Insights and My Direction beside them (Alex's default, 26 Nov
                2026), then Account (Settings), shortcuts, language, theme, help
                and Log out. Notifications is the Updates row above. */}
            <DropdownMenuContent side="right" align="end" sideOffset={22} className="nsu-nav-account-menu">
              <DropdownMenuGroup>
                <DropdownMenuLabel className="nsu-nav-identity"><Avatar seed={props.settings.avatar || props.user.avatar} alt="" className="nsu-nav-menu-avatar" /><span><strong>{props.user.name}</strong><small>{email || 'Your NextStepUni account'}</small></span></DropdownMenuLabel>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem onClick={() => afterMenuCloses(nav.navigateToYearPlans)}><NavigationIcon name="yearplans" />Year Plans</DropdownMenuItem>
                <DropdownMenuItem onClick={() => afterMenuCloses(props.onOpenPassport)}><NavigationIcon name="passport" />Study Passport<span className="nsu-nav-menu-end nsu-nav-readout">{props.completedCount} / {props.totalCount}</span></DropdownMenuItem>
                <DropdownMenuItem onClick={() => afterMenuCloses(nav.navigateToYourSetup)}><NavigationIcon name="setup" />Your setup</DropdownMenuItem>
                <DropdownMenuItem onClick={() => afterMenuCloses(nav.navigateToInsights)}><NavigationIcon name="insights" />Insights</DropdownMenuItem>
                <DropdownMenuItem onClick={() => afterMenuCloses(props.onOpenDirection)}><NavigationIcon name="direction" />My Direction</DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem onClick={() => afterMenuCloses(props.onOpenSettings)}><NavigationIcon name="account" />Account</DropdownMenuItem>
                <DropdownMenuItem onClick={() => afterMenuCloses(openShortcutsOverlay)}><NavigationIcon name="keyboard" />Keyboard shortcuts<span className="nsu-nav-menu-end nsu-nav-readout">⌘ /</span></DropdownMenuItem>
                <DropdownMenuSub>
                  <DropdownMenuSubTrigger><NavigationIcon name="language" />Language</DropdownMenuSubTrigger>
                  <DropdownMenuSubContent className="nsu-nav-submenu"><DropdownMenuRadioGroup value={props.settings.language} onValueChange={() => props.updateSetting('language', 'en')}><DropdownMenuRadioItem value="en" data-sound="select">English</DropdownMenuRadioItem></DropdownMenuRadioGroup></DropdownMenuSubContent>
                </DropdownMenuSub>
                <DropdownMenuSub>
                  <DropdownMenuSubTrigger><NavigationIcon name="theme" />Theme</DropdownMenuSubTrigger>
                  <DropdownMenuSubContent className="nsu-nav-submenu"><DropdownMenuRadioGroup value={props.settings.darkMode ? 'dark' : 'light'} onValueChange={value => props.updateSetting('darkMode', value === 'dark')}><DropdownMenuRadioItem value="light" data-sound="toggleOff">Light</DropdownMenuRadioItem><DropdownMenuRadioItem value="dark" data-sound="toggleOn">Dark</DropdownMenuRadioItem></DropdownMenuRadioGroup></DropdownMenuSubContent>
                </DropdownMenuSub>
                <DropdownMenuSub>
                  <DropdownMenuSubTrigger><NavigationIcon name="help" />Help</DropdownMenuSubTrigger>
                  <DropdownMenuSubContent className="nsu-nav-submenu">
                    <DropdownMenuItem onClick={() => afterMenuCloses(props.onOpenSiteGuide)}>How the app works</DropdownMenuItem>
                    <DropdownMenuItem onClick={nav.navigateToAccreditation}>References</DropdownMenuItem>
                    <DropdownMenuItem onClick={() => afterMenuCloses(props.onOpenFeedback)}>Help us improve</DropdownMenuItem>
                  </DropdownMenuSubContent>
                </DropdownMenuSub>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuItem variant="destructive" onClick={props.onLogout}><NavigationIcon name="logout" />Log out</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarFooter>
      </Sidebar>
      {open && <SidebarResize width={sidebarWidth} minWidth={MIN_WIDTH} maxWidth={maxWidth} defaultWidth={DEFAULT_WIDTH} onWidthChange={setPreferredWidth} onResizingChange={handleResizingChange} />}
      <SidebarInset className="student-sidebar-page">{props.children}</SidebarInset>
      <NotificationBell uid={props.user.uid} variant="sidebar" returnFocusRef={updatesTrigger} onUnreadCountChange={props.onUnreadCountChange} />
    </SidebarProvider>
  </TooltipProvider></SoundScope>;
}

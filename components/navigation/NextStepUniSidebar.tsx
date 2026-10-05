import { Fragment, useCallback, useEffect, useRef, useState, type ReactNode, type PointerEvent, type CSSProperties } from 'react';
import { LayoutGroup, motion, useReducedMotion } from 'framer-motion';
import {
  SidebarProvider, Sidebar, SidebarHeader, SidebarContent, SidebarFooter,
  SidebarInset, SidebarTrigger, SidebarGroup, SidebarGroupLabel, SidebarGroupContent,
  SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarMenuBadge, SidebarSeparator,
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuGroup,
  DropdownMenuLabel, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuSub,
  DropdownMenuSubTrigger, DropdownMenuSubContent, DropdownMenuRadioGroup, DropdownMenuRadioItem,
  TooltipProvider, Kbd, useIsMobile, SoundEffects, SidebarResize,
} from '../kobra-navigation-runtime';
import { NavigationIcon, type NavigationIconName } from './NavigationIcon';
import { useNavigation } from '../../contexts/NavigationContext';
import { useMobileAppDesign } from '../../hooks/useMobileAppDesign';
import type { SessionUser } from '../../utils/authUtils';
import type { UserSettings } from '../../types';
import Avatar from '../Avatar';
import GetPointsButton from '../GetPointsButton';
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
  onUnreadCountChange: (count: number) => void;
  completedCount: number;
  totalCount: number;
  unreadCount: number;
}

type Item = { label: string; icon: NavigationIconName; active?: boolean; go: () => void; badge?: string; coach?: string };
const afterMenuCloses = (go: () => void) => window.setTimeout(go, 0);
const DEFAULT_WIDTH = 264;
const MIN_WIDTH = 192;
const MAX_WIDTH = 360;
const WIDTH_STORAGE_KEY = 'nextstepuni-sidebar-width';

/** Uses the current purchased Kobra parts. Only the destinations/brand composition are ours. */
export default function NextStepUniSidebar(props: Props) {
  const mobile = useIsMobile();
  const mobileAppDesign = useMobileAppDesign();
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
  const reduced = useReducedMotion();
  const { viewState, activeTool } = nav.state;
  const email = auth.currentUser?.uid === props.user.uid ? auth.currentUser.email : null;
  const tool = (id: string) => viewState === 'innovation-zone' && activeTool === id;
  const groups: { title?: string; items: Item[] }[] = [
    { items: [
      { label: 'Home', icon: 'home', active: viewState === 'tree', go: nav.navigateToTree },
      { label: 'Modules', icon: 'modules', active: ['modules', 'category'].includes(viewState), go: nav.navigateToModules, coach: 'modules' },
      { label: 'Study session', icon: 'timer', active: viewState === 'study-session', go: nav.navigateToStudySession, coach: 'study' },
    ] },
    { title: 'Workspace', items: [
      { label: 'Launchpad', icon: 'compass', active: viewState === 'innovation-zone' && !['planner', 'mark-bank', 'topic-atlas', 'paper-trail', 'war-room', 'syllabus-xray', 'future-finder', 'future-finder-revamped'].includes(activeTool ?? ''), go: () => nav.navigateToInnovationZone(), coach: 'launchpad' },
      { label: 'Mark Bank', icon: 'marks', active: tool('mark-bank'), go: () => nav.navigateToInnovationZone('mark-bank') },
      { label: 'Planner', icon: 'planner', active: tool('planner'), go: () => nav.navigateToInnovationZone('planner') },
      { label: 'Topic Atlas', icon: 'atlas', active: tool('topic-atlas'), go: () => nav.navigateToInnovationZone('topic-atlas') },
      { label: 'Paper Trail', icon: 'papers', active: tool('paper-trail'), go: () => nav.navigateToInnovationZone('paper-trail') },
    ] },
    { title: 'Your journey', items: [
      { label: 'Learning paths', icon: 'paths', active: viewState === 'learning-paths', go: nav.navigateToLearningPaths },
      { label: 'My Progress', icon: 'progress', active: ['dashboard', 'insights'].includes(viewState), go: () => nav.navigateToDashboard() },
      { label: 'My Island', icon: 'island', active: viewState === 'my-journey', go: nav.navigateToJourney },
      { label: 'War Room', icon: 'target', active: tool('war-room') || tool('syllabus-xray'), go: () => nav.navigateToInnovationZone('war-room') },
      { label: 'Future Finder', icon: 'directions', active: tool('future-finder-revamped') || tool('future-finder'), go: () => nav.navigateToInnovationZone('future-finder-revamped') },
      { label: 'Study Passport', icon: 'passport', go: props.onOpenPassport, badge: `${props.completedCount}/${props.totalCount}` },
      { label: 'Year Plans', icon: 'yearplans', active: viewState === 'year-plans', go: nav.navigateToYearPlans },
      { label: 'References', icon: 'references', active: viewState === 'accreditation', go: nav.navigateToAccreditation },
    ] },
  ];

  const highlight = (event: PointerEvent<HTMLDivElement>) => {
    const item = (event.target as Element).closest<HTMLElement>('[data-slot="sidebar-menu-item"]');
    if (!item || !content.current) return setHover(null);
    const row = item.getBoundingClientRect();
    const parent = content.current.getBoundingClientRect();
    setHover({ x: row.left - parent.left, y: row.top - parent.top + content.current.scrollTop, width: row.width, height: row.height });
  };

  // Mobile keeps its native bottom bar and profile sheet. No desktop sidebar shortcut is mounted.
  if (mobile || mobileAppDesign) return <>{props.children}<div className="hidden"><NotificationBell uid={props.user.uid} onUnreadCountChange={props.onUnreadCountChange} /></div></>;

  const SoundScope = typeof globalThis.AudioContext === 'function' ? SoundEffects : Fragment;
  return <SoundScope><TooltipProvider>
    <SidebarProvider open={open} onOpenChange={setOpen} className="nsu-kobra-nav student-sidebar-shell" data-resizing={resizing || undefined} data-compact={open && sidebarWidth < 224 || undefined} style={{ '--sidebar-width': `${sidebarWidth}px`, '--sidebar-width-icon': '48px', '--navigation-width': open ? `${sidebarWidth}px` : '64px' } as CSSProperties}>
      <Sidebar variant="inset" collapsible="icon" className="nsu-nav-container">
        <SidebarHeader className="nsu-nav-header">
          <div className="nsu-nav-brand-row">
            <button type="button" className="nsu-nav-wordmark" data-sound="select" onClick={nav.navigateToTree} aria-label="NextStepUni home">nextstepuni</button>
            <SidebarTrigger className="nsu-nav-collapse" data-sound={open ? 'close' : 'open'} aria-label={open ? 'Collapse sidebar' : 'Expand sidebar'} aria-expanded={open} />
          </div>
        </SidebarHeader>
        <LayoutGroup id="nextstepuni-navigation">
          <SidebarContent ref={content} className="nsu-nav-content" onPointerOver={highlight} onPointerLeave={() => setHover(null)} onScroll={() => setHover(null)}>
            {hover && <motion.span aria-hidden="true" className="nsu-nav-hover" initial={false} animate={{ x: hover.x, y: hover.y, width: hover.width, height: hover.height }} transition={{ duration: reduced ? 0 : .15, ease: [.16, 1, .3, 1] }} />}
            <nav aria-label="Main navigation">
              {groups.map((group, index) => <Fragment key={group.title ?? 'main'}>
                {index > 0 && <SidebarSeparator className="nsu-nav-divider" />}
                <SidebarGroup className="nsu-nav-group">
                  {group.title && <SidebarGroupLabel className="nsu-nav-group-label">{group.title}</SidebarGroupLabel>}
                  <SidebarGroupContent><SidebarMenu>
                    {group.items.map(item => <SidebarMenuItem key={item.label} className="nsu-nav-item">
                      {item.active && <motion.span layoutId="active-line" className="nsu-nav-active-line" transition={reduced ? { duration: 0 } : { type: 'spring', duration: .35, bounce: 0 }} aria-hidden="true" />}
                      <SidebarMenuButton isActive={item.active} className="nsu-nav-button" data-sound="select" aria-label={item.label} aria-current={item.active ? 'page' : undefined} tooltip={open ? undefined : item.label} data-coach={item.coach} onClick={item.go} render={<motion.button whileTap={reduced ? undefined : 'pressed'} />}>
                        <motion.span variants={{ pressed: { scale: .9 } }} transition={{ type: 'spring', duration: .3, bounce: .25 }} className="nsu-nav-symbol"><NavigationIcon name={item.icon} active={item.active} /></motion.span>
                        <span className="nsu-nav-label">{item.label}</span>
                      </SidebarMenuButton>
                      {item.badge && <SidebarMenuBadge className="nsu-nav-badge">{item.badge}</SidebarMenuBadge>}
                    </SidebarMenuItem>)}
                  </SidebarMenu></SidebarGroupContent>
                </SidebarGroup>
              </Fragment>)}
            </nav>
          </SidebarContent>
        </LayoutGroup>
        <SidebarFooter className="nsu-nav-footer">
          <div className="nsu-nav-points"><GetPointsButton uid={props.user.uid} expanded={open} icon={<NavigationIcon name="points" />} label="Get points" sound="chirp" /></div>
          <DropdownMenu>
            <DropdownMenuTrigger ref={accountTrigger} className="nsu-nav-account" aria-label="Open account menu" data-coach="help">
              <Avatar seed={props.settings.avatar || props.user.avatar} alt="" className="nsu-nav-avatar" />
              {props.unreadCount > 0 && <span className="nsu-nav-unread-dot" aria-label={`${props.unreadCount} unread notifications`} />}
              <span className="nsu-nav-account-copy"><span>{props.user.name}</span><small>{props.user.isAdmin ? 'Admin' : 'Student'}</small></span>
              <svg viewBox="0 0 20 20" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.5" aria-hidden="true" className="nsu-nav-account-chevron"><path d="m6 8 4-4 4 4M6 12l4 4 4-4" /></svg>
            </DropdownMenuTrigger>
            <DropdownMenuContent side="top" align="start" sideOffset={8} className="nsu-nav-account-menu">
              <DropdownMenuGroup>
                <DropdownMenuLabel className="nsu-nav-identity"><Avatar seed={props.settings.avatar || props.user.avatar} alt="" className="nsu-nav-menu-avatar" /><span><strong>{props.user.name}</strong><small>{email || 'Your NextStepUni account'}</small></span></DropdownMenuLabel>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
                <DropdownMenuItem onClick={() => afterMenuCloses(props.onOpenSettings)}><NavigationIcon name="account" />Account</DropdownMenuItem>
                <DropdownMenuItem data-notification-toggle onClick={() => afterMenuCloses(toggleNotificationPanel)}><NavigationIcon name="bell" />Notifications{props.unreadCount > 0 && <span className="nsu-nav-notification-count">{props.unreadCount > 99 ? '99+' : props.unreadCount}</span>}</DropdownMenuItem>
                <DropdownMenuItem onClick={() => afterMenuCloses(openShortcutsOverlay)}><NavigationIcon name="keyboard" />Keyboard shortcuts<span className="nsu-nav-shortcut"><Kbd>⌘</Kbd><Kbd>/</Kbd></span></DropdownMenuItem>
              </DropdownMenuGroup>
              <DropdownMenuSeparator />
              <DropdownMenuGroup>
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
      <NotificationBell uid={props.user.uid} variant="sidebar" returnFocusRef={accountTrigger} onUnreadCountChange={props.onUnreadCountChange} />
    </SidebarProvider>
  </TooltipProvider></SoundScope>;
}

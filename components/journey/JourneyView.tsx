import React, { useMemo, useRef, useState } from "react";
import {
  ArrowLeft,
  ArrowUpRight,
  BookOpen,
  Check,
  Compass,
  Hammer,
  Map,
  X,
} from "lucide-react";
import type { NorthStar, UserProgress } from "../../types";
import type { SessionUser } from "../../utils/authUtils";
interface CourseInfo {
  id: string;
  sectionsCount: number;
}
import Avatar from "../Avatar";
import JourneyWelcome from "./JourneyWelcome";
import { usePaperIsland } from "../../hooks/usePaperIsland";
import {
  knownLandmarks,
  axialDistance,
  paperTileKind,
  PAPER_LANDMARKS,
  type PaperDiscoveryId,
} from "../../functions/src/paperIslandModel";
import {
  IslandMap,
  TileShelf,
  Placement,
  Overlay,
  defaultCamera,
} from "./paper/MapControls";
import { piece } from "./paper/studioModel";
import { tileById, type TileKind } from "./paper/catalogue";
import {
  discoveries,
  visibleDiscoveries,
  discoveryRoute,
  nextDiscovery,
  buildable,
  frontier,
  groupFor,
  type ShelfGroup,
} from "./paper/model";
import { coastalMap, legendById, type LegendId } from "./paper/collection";
import { StickerArt } from "./paper/StickerArt";
import { TilePortrait } from "./paper/TileArt";
import { centre } from "./paper/geometry";
import { crewArt, crewById, journeyCrew, visitorHasAnchor, visitorWishFulfilled, wishText, type CrewId } from "./visitors/catalogue";
import { VisitorsBook, WondersBook } from "./visitors/VisitorsBook";
import { VisitorPanel, type VisitorPage } from "./visitors/VisitorPanel";
import "./paper/paper.css";
import "./visitors/visitors.css";

interface JourneyViewProps {
  onBack: () => void;
  user: SessionUser;
  hasSeenWelcome: boolean;
  onDismissWelcome: () => void;
  northStar: NorthStar | null;
  onOpenNorthStar: () => void;
  pointsBalance: number;
  onPointsReload: () => void;
  userProgress?: UserProgress;
  allCourses?: CourseInfo[];
  subjects?: string[];
}
interface JourneyNotice {
  id: string;
  title: string;
  detail: string;
}
export default function JourneyView({ user, onBack, hasSeenWelcome, onDismissWelcome }: JourneyViewProps) {
  const { island, balance, busy, error, execute } = usePaperIsland(user.uid);
  const [building, setBuilding] = useState(false),
    [chosen, setChosen] = useState<TileKind>("meadow"),
    [candidate, setCandidate] = useState<string | null>(null),
    [camera, setCamera] = useState(defaultCamera),
    [group, setGroup] = useState<ShelfGroup>("All tiles"),
    [notice, setNotice] = useState<JourneyNotice | null>(null);
  const [chosenWonder,setChosenWonder]=useState<CrewId|null>(null);
  const [fieldbookSection,setFieldbookSection]=useState<"stories"|"visitors"|"wonders">("stories");
  const [visitor,setVisitor]=useState<CrewId>("luma"),[visitorPage,setVisitorPage]=useState<VisitorPage>("visit");
  const [panel, setPanel] = useState<
      "fieldbook" | "points" | "tile" | "discovery" | "treasure" | "visitor" | null
    >(null),
    [inspected, setInspected] = useState<TileKind>("meadow"),
    [discovery, setDiscovery] = useState<LegendId>("lantern-nautilus");
  const [treasure, setTreasure] = useState("");
  const currentVisitor=useRef(visitor),currentPanel=useRef(panel);
  currentVisitor.current=visitor;currentPanel.current=panel;
  const placed = useMemo(
    () =>
      island
        ? [
            ...island.tiles.map((t) => piece(t.q, t.r, paperTileKind(t), t.edge, t.wonderId)),
            ...knownLandmarks(island.tiles).map((t) => piece(t.q, t.r, t.kind)),
          ]
        : [],
    [island?.tiles],
  );
  const world = useMemo(
    () => ({
      placed,
      balance,
      credits: island?.credits ?? 0,
      history: island?.undo ? [island.undo] : [],
      log:
        island?.tiles
          .filter((t) => t.cost > 0)
          .map((t) => ({ kind: paperTileKind(t), cost: t.cost })) ?? [],
    }),
    [placed, balance, island],
  );
  const seen = visibleDiscoveries(placed),
    selected = tileById[chosen],
    kept = island?.kept ?? [];
  const claimedVisitors=island?.claimedVisitors??[];
  const waitingVisitors=island?journeyCrew.filter(crew=>!claimedVisitors.includes(crew.id)&&((island.metVisitors??[]).includes(crew.id)||visitorHasAnchor(island.tiles,crew.id))):[];
  const visiting=waitingVisitors.find(crew=>(island?.metVisitors??[]).includes(crew.id)&&visitorWishFulfilled(island!.tiles,crew.id))??waitingVisitors[0];
  const visitorAnchor=visiting?island?.tiles.find(tile=>!tile.wonderId&&tile.kind===visiting.anchor):undefined;
  const openVisitor=(id:CrewId,page:VisitorPage="visit")=>{setVisitor(id);setVisitorPage(page);setPanel("visitor");setNotice(null);};
  const changeMode = (value: boolean) => {
    setBuilding(value);
    setCandidate(null);
    setNotice(null);
    if (!value) { setChosenWonder(null);if(group==="Wonder tiles")setGroup("All tiles"); }
  };
  const choose = (kind: TileKind) => {
    setChosen(kind);
    setChosenWonder(null);
    setNotice(null);
  };
  const build = async () => {
    if (!candidate || !island) return;
    const [q, r] = candidate.split(",").map(Number);
    if (
      await execute({
        ...(chosenWonder?{action:"placeWonder" as const,id:chosenWonder}:{action:"place" as const,kind:chosen}),
        q,
        r,
        requestId: crypto.randomUUID(),
        revision: island.revision,
      })
    ) {
      setCandidate(null);
      if (chosenWonder) {
        setNotice({id:crypto.randomUUID(),title:`${crewById[chosenWonder].wonder} ${island.tiles.some(tile=>tile.wonderId===chosenWonder)?"moved":"added"}.`,detail:"A gift from a wanderer, now part of your world."});
        return;
      }
      const nextTiles=[...island.tiles,{q,r,kind:chosen==="capybara"?"water" as const:chosen}];
      const readyVisitor=journeyCrew.find(crew=>(island.metVisitors??[]).includes(crew.id)&&!claimedVisitors.includes(crew.id)&&!visitorWishFulfilled(island.tiles,crew.id)&&visitorWishFulfilled(nextTiles,crew.id));
      const found = visibleDiscoveries([...placed, piece(q, r, chosen)])
        .find(d => !seen.some(previous => previous.id === d.id));
      if (readyVisitor) {
        openVisitor(readyVisitor.id);
      } else if (found) {
        setNotice(null);
        showDiscovery(found.id);
      } else {
        setNotice({
          id: crypto.randomUUID(),
          title: `${selected.name} added.`,
          detail: "A little more of the map is yours to explore.",
        });
      }
    }
  };
  const undo = async () => {
    if (!island) return;
    if (
      await execute({
        action: "undo",
        requestId: crypto.randomUUID(),
        revision: island.revision,
      })
    ) {
      setCandidate(null);
      setNotice({
        id: crypto.randomUUID(),
        title: "Last tile returned.",
        detail: "Your points or earned tile have been returned too.",
      });
    }
  };
  const showDiscovery = (id: LegendId) => {
    setDiscovery(id);
    setPanel("discovery");
  };
  const chooseWonder=(id:CrewId)=>{
    setChosenWonder(id);setChosen("meadow");setGroup("Wonder tiles");setCandidate(null);setNotice(null);setPanel(null);setBuilding(true);
    const existing=island?.tiles.find(tile=>tile.wonderId===id);
    if(existing) { const pos=centre(existing.q,existing.r);setCamera({...pos,y:pos.y-75,zoom:1}); }
  };
  const buildVisitorWish=(id:CrewId,anchorOnly=false)=>{
    if(!island)return;
    const crew=crewById[id],ordinary=island.tiles.filter(tile=>!tile.wonderId),slots=frontier(placed);
    let kind=anchorOnly?crew.anchor:crew.tile;
    let spot=slots.find(slot=>ordinary.some(tile=>tile.kind===(anchorOnly?crew.tile:crew.anchor)&&axialDistance(tile,slot)===1));
    if(!spot&&!anchorOnly) {
      kind=crew.anchor;
      spot=slots.find(slot=>ordinary.some(tile=>tile.kind===crew.tile&&axialDistance(tile,slot)===1));
    }
    spot??=slots[0];
    choose(kind);setGroup(groupFor(kind));setBuilding(true);setPanel(null);setCandidate(spot?.key??null);
    if(spot)setCamera({x:spot.x,y:spot.y-75,zoom:1});
    setNotice({id:crypto.randomUUID(),title:`${crew.name}’s little wish.`,detail:kind===crew.tile?wishText(id):`Add ${crew.anchorLabel.toLowerCase()} to make a little room for ${crew.name}.`});
  };
  const findSticker = (id?: LegendId) => {
    const target = id ? discoveries.find(d => d.id === id) : undefined;
    const route = target
      ? { discovery: target, path: discoveryRoute(placed, target) }
      : nextDiscovery(placed, kept);
    if (!route?.path) return;
    if (!route.path.length) { showDiscovery(route.discovery.id); return; }
    const next = route.path[0];
    setPanel(null);
    setBuilding(true);
    setChosen("meadow");
    setChosenWonder(null);
    setGroup("All tiles");
    setCandidate(next.key);
    setCamera({ x: next.x, y: next.y - 75, zoom: 1 });
    setNotice({
      id: crypto.randomUUID(),
      title: "Your next discovery.",
      detail: route.path.length === 1
        ? "Place a tile in the highlighted corner to uncover a mythic sticker."
        : `Start at the highlighted corner. A mythic sticker is ${route.path.length} placements away along this route.`,
    });
  };
  return (
    <div
      className={`journey-paper island-views coast tone-pencilatlas ${building ? "is-building" : "is-viewing"}`}
    >
      <main className="student-app">
        <header className="student-nav journey-nav-with-help">
          <button className="student-wordmark" onClick={onBack}>
            nextstepuni
          </button>
          <span className="nav-divider" />
          <button className="launchpad-link" onClick={onBack}>
            <ArrowLeft size={15} /> Home
          </button>
          <div className="nav-spacer" />
          <JourneyWelcome hasSeenWelcome={hasSeenWelcome} onDismissWelcome={onDismissWelcome} />
          <button
            className="island-wallet"
            aria-label={`Your balance: ${balance} Journey Points`}
            onClick={() => setPanel("points")}
          >
            <span className="jp-coin">JP</span>
            <strong data-jp-balance>{balance}</strong>
            <span>Journey Points</span>
          </button>
          <button
            className="student-avatar"
            aria-label="Your character · open fieldbook"
            onClick={() => setPanel("fieldbook")}
          >
            <Avatar seed={user.avatar || user.name} alt="Your character" />
          </button>
        </header>
        <div className="coast-world">
          <div className="coast-map-area">
            {island ? (
              <IslandMap
                world={world}
                building={building}
                chosen={chosen}
                chosenWonder={chosenWonder}
                candidate={candidate}
                onCandidate={setCandidate}
                onInspect={(kind) => {
                  setInspected(kind);
                  setPanel("tile");
                }}
                onDiscover={showDiscovery}
                onInspectWonder={id=>openVisitor(id,"wonder")}
                visitor={visiting&&visitorAnchor?{id:visiting.id,q:visitorAnchor.q,r:visitorAnchor.r}:undefined}
                onVisit={openVisitor}
                onTreasure={(id) => {
                  setTreasure(id);
                  setPanel("treasure");
                }}
                camera={camera}
                setCamera={setCamera}
              />
            ) : (
              <div className="paper-loading" role="status">
                <TilePortrait kind="home" />
                <p>
                  {busy
                    ? "Opening your island…"
                    : "Your island could not be opened."}
                </p>
                {!busy && (
                  <button
                    className="primary-action"
                    onClick={() => void execute({ action: "open" })}
                  >
                    Try again
                  </button>
                )}
              </div>
            )}
            {!building && island && (
              <div className="island-dock">
                <button
                  aria-label="Your island"
                  onClick={() => setCamera(defaultCamera)}
                >
                  <Map size={18} />
                  <span>Your island</span>
                </button>
                <button onClick={() => setPanel("fieldbook")}>
                  <BookOpen size={18} />
                  <span>Fieldbook</span>
                  <small>{seen.length}</small>
                </button>
                {kept.length < discoveries.length && <button
                  className="sticker-finder"
                  aria-label="Find a sticker"
                  title="Find a sticker"
                  onClick={() => findSticker()}
                >
                  <Compass size={18} /><span>Find a sticker</span>
                </button>}
                <button className="visitor-dock" aria-label="Wandering visitors" title="Wandering visitors" onClick={()=>{setFieldbookSection("visitors");setPanel("fieldbook");}}><img src={crewArt(visiting?.id??"luma")} alt="" width="35" height="35"/><span>Visitors</span>{waitingVisitors.length>0&&<small>{waitingVisitors.length}</small>}</button>
                <button
                  className="primary-action"
                  aria-label="Build your island"
                  onClick={() => changeMode(true)}
                >
                  <Hammer size={17} /><span className="desktop-build-label">Build your island</span><span className="mobile-build-label">Build</span>
                </button>
              </div>
            )}
            <button
              className="coast-done quiet-action"
              hidden={!building}
              onClick={() => changeMode(false)}
            >
              Done <Check size={15} />
            </button>
            {(notice || error) && (
              <div
                key={error || notice?.id}
                className="island-notice"
                role={error ? "alert" : "status"}
                aria-atomic="true"
              >
                <div className="island-notice-copy">
                  <strong>{error ? "Couldn’t update your island." : notice?.title}</strong>
                  <p>{error || notice?.detail}</p>
                </div>
                {!error && (
                  <button aria-label="Dismiss update" onClick={() => setNotice(null)}>
                    <X size={16} />
                  </button>
                )}
              </div>
            )}
          </div>
          <div
            className="coast-build-tray"
            inert={!building}
            aria-hidden={!building}
          >
            <TileShelf
              chosen={chosen}
              chosenWonder={chosenWonder}
              wonders={claimedVisitors}
              onChooseWonder={chooseWonder}
              onChoose={choose}
              balance={balance}
              credits={world.credits}
              group={group}
              setGroup={setGroup}
              orientation="row"
            />
            <Placement
              world={world}
              chosen={chosen}
              chosenWonder={chosenWonder}
              candidate={candidate}
              onPlace={() => void build()}
              onUndo={() => void undo()}
              busy={busy}
            />
          </div>
        </div>
      </main>
      {panel && (
        <Overlay
          title={
            panel === "fieldbook"
              ? "Your fieldbook"
              : panel === "points"
                ? "Your Journey Points"
                : panel === "tile"
                ? tileById[inspected].name
                : panel === "visitor"
                  ? `${crewById[visitor].name} · ${crewById[visitor].role}`
                  : panel === "treasure"
                    ? "A treasure, found"
                    : legendById[discovery].name
          }
          onClose={() => setPanel(null)}
          className={panel==="visitor"?"has-visitor":panel==="fieldbook"&&fieldbookSection!=="stories"?"has-visitors-book":""}
        >
          {panel === "fieldbook" && (
            <>
            <nav className="fieldbook-tabs" aria-label="Fieldbook sections">{([['stories','Stories'],['visitors','Visitors'],['wonders','Wonder tiles']] as const).map(([section,label])=><button key={section} aria-pressed={fieldbookSection===section} onClick={()=>setFieldbookSection(section)}>{label}</button>)}</nav>
            {fieldbookSection==="stories"&&(
            <div className="fieldbook-panel">
              <span className="eyebrow">YOUR FIELD NOTES</span>
              <h2>
                Things found
                <br />
                <em>along the way.</em>
              </h2>
              <p>
                Mythic stickers come into view as your island grows. Choose an
                undiscovered story below and we’ll point out a corner to build
                towards it.
              </p>
              <div className="fieldbook-discoveries">
                {discoveries.map((d) => {
                  const visible = seen.some((s) => s.id === d.id);
                  return (
                    <button
                      key={d.id}
                      onClick={() => visible ? showDiscovery(d.id) : findSticker(d.id)}
                    >
                      {visible ? (
                        <StickerArt id={d.id} />
                      ) : (
                        <span className="unknown-discovery">
                          <Compass size={29} />
                        </span>
                      )}
                      <span>
                        <strong>
                          {visible
                            ? legendById[d.id].name
                            : "Somewhere in the mist"}
                        </strong>
                        <small>
                          {visible
                            ? kept.includes(d.id)
                              ? "Kept in your fieldbook"
                              : "In sight · take a closer look"
                            : "Show me the way"}
                        </small>
                      </span>
                      <ArrowUpRight size={18} />
                    </button>
                  );
                })}
              </div>
            </div>)}
            {island&&fieldbookSection==="visitors"&&<VisitorsBook island={island} onVisit={openVisitor}/>}
            {island&&fieldbookSection==="wonders"&&<WondersBook island={island} onWonder={id=>openVisitor(id,"wonder")}/>}
            </>
          )}
          {panel==="visitor"&&island&&<VisitorPanel id={visitor} page={visitorPage} island={island} busy={busy} error={error} onPage={setVisitorPage} onClose={()=>setPanel(null)} onBuildAnchor={()=>buildVisitorWish(visitor,true)} onBuildWish={()=>buildVisitorWish(visitor)} onPlaceWonder={()=>chooseWonder(visitor)}
            onMeet={()=>void execute({action:"meetVisitor",id:visitor})}
            onClaim={()=>{const id=visitor;void execute({action:"claimVisitor",id}).then(saved=>{if(saved&&currentVisitor.current===id&&currentPanel.current==="visitor")setVisitorPage("gift");});}}
          />}
          {panel === "points" && (
            <div className="points-panel">
              <span className="eyebrow">YOUR JOURNEY POINTS</span>
              <h2>
                A little study.
                <br />
                <em>A little more world.</em>
              </h2>
              <strong>
                {balance}
                <small> JP</small>
              </strong>
              <p>
                Earn points as you study, then choose what to add to your
                island. There’s no upkeep to pay. New ranks give you three
                meadow tiles to place wherever you like.
              </p>
              <dl>
                <div>
                  <dt>In your pocket</dt>
                  <dd>{balance} JP</dd>
                </div>
                <div>
                  <dt>Spent on this island</dt>
                  <dd>
                    {world.log.reduce((sum, item) => sum + item.cost, 0)} JP
                  </dd>
                </div>
                <div>
                  <dt>Meadow tiles earned</dt>
                  <dd>{world.credits}</dd>
                </div>
              </dl>
              <button
                className="primary-action"
                onClick={() => {
                  setPanel(null);
                  changeMode(true);
                }}
              >
                Find your next tile <ArrowUpRight size={18} />
              </button>
            </div>
          )}
          {panel === "tile" && (
            <div className="tile-detail-panel">
              <TilePortrait kind={inspected} />
              <span className="eyebrow">PART OF YOUR WORLD</span>
              <h2>{tileById[inspected].name}</h2>
              <p>{tileById[inspected].description}</p>
              {buildable.some((t) => t.id === inspected) && (
                <button
                  className="primary-action"
                  onClick={() => {
                    choose(inspected);
                    changeMode(true);
                    setPanel(null);
                  }}
                >
                  Build another · {tileById[inspected].price} JP{" "}
                  <ArrowUpRight size={17} />
                </button>
              )}
            </div>
          )}
          {panel === "treasure" && (
            <div className="tile-detail-panel">
              <TilePortrait kind="treasure" />
              <span className="eyebrow">OFF THE BEATEN PATH</span>
              <h2>{PAPER_LANDMARKS.find((d) => d.id === treasure)?.name}</h2>
              <p>
                Someone left a little room to grow. Open this chest to collect
                two meadow tiles. Opening a chest keeps the path you built to
                reach it.
              </p>
              <button
                className="primary-action"
                disabled={
                  busy || (island?.claimedCaches ?? []).includes(treasure)
                }
                onClick={() => void execute({ action: "claim", id: treasure })}
              >
                {(island?.claimedCaches ?? []).includes(treasure)
                  ? "Treasure collected"
                  : "Open the chest"}{" "}
                <Check size={17} />
              </button>
            </div>
          )}
          {panel === "discovery" && (
            <div className="discovery-detail-panel">
              <div style={{ backgroundImage: `url(${coastalMap})` }}>
                <StickerArt id={discovery} />
              </div>
              <section>
                <span className="eyebrow">A LITTLE SOMETHING, FOUND</span>
                <h2>{legendById[discovery].name}</h2>
                <p>{legendById[discovery].story}</p>
                <button
                  className="primary-action"
                  disabled={
                    busy || kept.includes(discovery as PaperDiscoveryId)
                  }
                  aria-pressed={kept.includes(discovery as PaperDiscoveryId)}
                  onClick={() =>
                    void execute({
                      action: "keep",
                      id: discovery as PaperDiscoveryId,
                    })
                  }
                >
                  {kept.includes(discovery as PaperDiscoveryId)
                    ? "Kept in your fieldbook"
                    : "Keep this story"}
                  <Check size={17} />
                </button>
              </section>
            </div>
          )}
        </Overlay>
      )}
    </div>
  );
}

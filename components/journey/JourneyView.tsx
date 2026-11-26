import React, { useLayoutEffect, useMemo, useRef, useState } from "react";
import { Compass, X } from "lucide-react";
import type { NorthStar, UserProgress } from "../../types";
import type { SessionUser } from "../../utils/authUtils";
interface CourseInfo {
  id: string;
  sectionsCount: number;
}
import JourneyWelcome from "./JourneyWelcome";
import BuildDrawer from "./BuildDrawer";
import KobraScope from "../approved-ui-runtime";
import PageHeader from "../ui/PageHeader";
import { TopBar } from "../ui/Bars";
import { Button, IconButton, TextButton } from "../ui/Button";
import { SelectionBar, SelectionWords } from "../ui/Choice";
import { List, Row } from "../ui/List";
import { Sheet } from "../ui/Sheet";
import { useMobileAppDesign } from "../../hooks/useMobileAppDesign";
import { usePaperIsland } from "../../hooks/usePaperIsland";
import {
  knownLandmarks,
  axialDistance,
  paperTileKind,
  paperRemovalBlock,
  paperReplaceCost,
  paperTileRefund,
  PAPER_LANDMARKS,
  type PaperDiscoveryId,
  type PaperTile,
} from "../../functions/src/paperIslandModel";
import {
  IslandMap,
  TileShelf,
  Placement,
  TileEditor,
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
import { crewById, journeyCrew, visitorHasAnchor, visitorWishFulfilled, wishText, type CrewId } from "./visitors/catalogue";
import { VisitorsBook, WondersBook } from "./visitors/VisitorsBook";
import { VisitorPanel, type VisitorPage } from "./visitors/VisitorPanel";
import { useYearIslands } from "../../hooks/useYearIslands";
import { DEMO_STUDENT_UID } from "../../data/devStudent";
import { getSchoolName } from "../../schoolData";
import { YearIslandsBook } from "./year/YearIslandsBook";
import { ClassmateIsland } from "./year/ClassmateIsland";
import { cohortLabel, type YearIsland } from "./year/yearIslands";
import "./paper/paper.css";
import "./visitors/visitors.css";
import "./year/year.css";
import "./journey-workspace.css";
import "./journey-frame.css";

/** The four parts of the island, in its one selection bar. */
type JourneySection = "island" | "build" | "fieldbook" | "year";

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
  /** Your setup, where a student without a school year can add one. */
  onOpenSetup?: () => void;
}
interface JourneyNotice {
  id: string;
  title: string;
  detail: string;
}
export default function JourneyView({ user, onBack, hasSeenWelcome, onDismissWelcome, onOpenSetup }: JourneyViewProps) {
  const { island, balance, busy, error, execute } = usePaperIsland(user.uid);
  const phone = useMobileAppDesign();
  // Year islands: a classmate's island being visited, look only. Building
  // always happens on your own island, so every way into build mode (the dock,
  // the fieldbook, a visitor's wish, a Wonder) ends the visit first.
  const [classmate, setClassmate] = useState<YearIsland | null>(null);
  const [building, setBuildingMode] = useState(false),
    [chosen, setChosen] = useState<TileKind>("meadow"),
    [candidate, setCandidate] = useState<string | null>(null),
    // Build mode: the placed tile (cell key) being swapped or removed.
    [editing, setEditing] = useState<string | null>(null),
    [camera, setCamera] = useState(defaultCamera),
    [group, setGroup] = useState<ShelfGroup>("All tiles"),
    [notice, setNotice] = useState<JourneyNotice | null>(null);
  const setBuilding = (value: boolean) => {
    if (value) setClassmate(null);
    setBuildingMode(value);
  };
  const [chosenWonder,setChosenWonder]=useState<CrewId|null>(null);
  const [fieldbookSection,setFieldbookSection]=useState<"stories"|"visitors"|"wonders">("stories");
  const [visitor,setVisitor]=useState<CrewId>("luma"),[visitorPage,setVisitorPage]=useState<VisitorPage>("visit");
  const [panel, setPanel] = useState<
      "fieldbook" | "points" | "tile" | "discovery" | "treasure" | "visitor" | "year" | null
    >(null),
    [inspected, setInspected] = useState<TileKind>("meadow"),
    [discovery, setDiscovery] = useState<LegendId>("lantern-nautilus");
  const [treasure, setTreasure] = useState("");
  const year = useYearIslands(user.uid, { enabled: panel === "year" });
  const yearSchool = year.cohort?.school ?? user.school;
  const cohort = cohortLabel(yearSchool, year.cohort?.yearGroup ?? user.yearGroup);
  const showYear = Boolean(user.school) || user.uid === DEMO_STUDENT_UID;
  const visitClassmate = (next: YearIsland) => { setClassmate(next); setPanel(null); setNotice(null); };
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
    setEditing(null);
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
    const last = island.undo;
    if (
      await execute({
        action: "undo",
        requestId: crypto.randomUUID(),
        revision: island.revision,
      })
    ) {
      setCandidate(null);
      setEditing(null);
      setNotice(
        last?.previousTile && !last.tileId
          ? { id: crypto.randomUUID(), title: "Tile put back.", detail: "It is back where it was, and its points or earned tile with it." }
          : last?.previousTile && !last.previousTile.wonderId && last.restoreCost !== undefined
            ? { id: crypto.randomUUID(), title: "Swap undone.", detail: "Your original tile is back, and your points with it." }
            : { id: crypto.randomUUID(), title: "Last tile returned.", detail: "Your points or earned tile have been returned too." },
      );
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
  const tileName = (tile: PaperTile) =>
    tile.wonderId ? crewById[tile.wonderId].wonder : tileById[paperTileKind(tile)].name;
  const editable = useMemo(
    () => new globalThis.Map((island?.tiles ?? []).filter(tile => tile.kind !== "home").map(tile => [`${tile.q},${tile.r}`, tileName(tile)] as const)),
    [island?.tiles],
  );
  const editingTile = editing ? island?.tiles.find(tile => `${tile.q},${tile.r}` === editing) : undefined;
  const selectTile = (key: string) => {
    setEditing(current => (current === key ? null : key));
    setCandidate(null);
    setNotice(null);
  };
  const pickCorner = (key: string) => {
    setCandidate(key);
    setEditing(null);
  };
  const editor = (() => {
    if (!island || !editingTile) return null;
    const refund = paperTileRefund(editingTile);
    const removeBlock = paperRemovalBlock(island.tiles, editingTile.id);
    const removeNote = refund.credit
      ? "Returns 1 earned tile"
      : refund.jp > 0
        ? `Returns ${refund.jp} JP`
        : editingTile.wonderId
          ? "Back to your Wonder tiles"
          : "Nothing to return";
    let replaceBlock: string | null = null, replaceNote = "";
    const price = chosenWonder ? null : paperReplaceCost(island, editingTile.id, chosen);
    const sameTile = !editingTile.wonderId && paperTileKind(editingTile) === chosen;
    if (chosenWonder || !price) replaceBlock = "Choose a tile from the shelf to swap in.";
    else if (sameTile) replaceBlock = "Choose a different tile from the shelf to swap in.";
    else if (price.net > balance)
      replaceBlock = `You need ${price.net - balance} more JP for this swap.`;
    if (price && !sameTile)
      replaceNote = price.usedCredit
        ? "1 earned tile"
        : price.net > 0
          ? `${price.net} JP`
          : price.net < 0
            ? `${-price.net} JP back`
            : "Even swap";
    // One sentence when both are blocked, so neither button is left unexplained.
    const note = removeBlock && sameTile && removeBlock.endsWith("or replace it.")
      ? "Remove the tiles beyond it first, or choose a different shelf tile to swap in."
      : removeBlock ?? replaceBlock;
    return { tile: editingTile, refund, removeNote, removeBlock, replaceNote, replaceBlock, note };
  })();
  const removeTile = async () => {
    if (!island || !editor) return;
    const name = tileName(editor.tile);
    if (await execute({ action: "remove", tileId: editor.tile.id, requestId: crypto.randomUUID(), revision: island.revision })) {
      setEditing(null);
      const { refund, tile } = editor;
      setNotice({
        id: crypto.randomUUID(),
        title: `${name} removed.`,
        detail: refund.credit
          ? "Your earned meadow tile is back on the shelf. Undo puts it back."
          : refund.jp > 0
            ? `${refund.jp} JP returned. Undo puts it back.`
            : tile.wonderId
              ? "It is back with your Wonder tiles, ready to place again."
              : "It was part of your starting island, so there is nothing to return. Undo puts it back.",
      });
    }
  };
  const replaceTile = async () => {
    if (!island || !editor) return;
    const from = tileName(editor.tile);
    if (await execute({ action: "replace", tileId: editor.tile.id, kind: chosen, requestId: crypto.randomUUID(), revision: island.revision })) {
      setNotice({ id: crypto.randomUUID(), title: `${from} swapped for ${selected.name}.`, detail: "Undo swaps it back." });
    }
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
  // One selection bar for the four parts of the island (c-world.html "c-world-journeybar"):
  // Build is build mode; the Fieldbook and Your year open in place under the bar; Island
  // takes you back. Every way in that the screen already had still works.
  const section: JourneySection = building ? "build" : panel === "fieldbook" ? "fieldbook" : panel === "year" ? "year" : "island";
  const goTo = (next: JourneySection) => {
    if (next === "build") { setPanel(null); if (!building) changeMode(true); return; }
    if (building) changeMode(false);
    if (next === "island") setClassmate(null);
    setNotice(null);
    setPanel(next === "island" ? null : next);
  };
  const sections: Array<{ value: JourneySection; label: string }> = [
    { value: "island", label: "Island" }, { value: "build", label: "Build" }, { value: "fieldbook", label: "Fieldbook" },
    ...(showYear ? [{ value: "year" as const, label: "Your year" }] : []),
  ];
  const bar = <SelectionBar<JourneySection> label="Journey sections" value={section} onChange={goTo} options={sections} className="jm-seg" />;
  const points = (
    <Button size="sm" className="jm-points" aria-label={`Your balance: ${balance} Journey Points`} onClick={() => setPanel("points")}>
      <span className="ui-readout"><span data-jp-balance>{balance.toLocaleString()}</span> JP</span>
    </Button>
  );
  const welcome = <JourneyWelcome hasSeenWelcome={hasSeenWelcome} onDismissWelcome={onDismissWelcome} trigger={phone ? "icon" : "text"} />;
  const inPlace = section === "fieldbook" || section === "year";
  const sheetPanel = panel && panel !== "fieldbook" && panel !== "year" ? panel : null;
  const sheetTitle = sheetPanel === "points" ? "Your Journey Points"
    : sheetPanel === "tile" ? tileById[inspected].name
      : sheetPanel === "visitor" ? `${crewById[visitor].name} · ${crewById[visitor].role}`
        : sheetPanel === "treasure" ? "A treasure, found"
          : legendById[discovery].name;
  const treasureOpened = (island?.claimedCaches ?? []).includes(treasure);
  const discoveryKept = kept.includes(discovery as PaperDiscoveryId);
  const sheetFooter = sheetPanel === "tile" && buildable.some((t) => t.id === inspected)
    ? <Button kind="main" size="lg" block arrow="forward" onClick={() => { choose(inspected); changeMode(true); setPanel(null); }}>{`Build another · ${tileById[inspected].price} JP`}</Button>
    : sheetPanel === "points"
      ? <Button kind="main" size="lg" block arrow="forward" onClick={() => { setPanel(null); changeMode(true); }}>Find your next tile</Button>
      : sheetPanel === "treasure"
        ? <Button kind="main" size="lg" block aria-busy={busy || undefined} unavailable={treasureOpened ? "Treasure collected: its two meadow tiles are on your shelf." : undefined}
            onClick={() => { if (!busy && !treasureOpened) void execute({ action: "claim", id: treasure }); }}>{treasureOpened ? "Treasure collected" : "Open the chest"}</Button>
        : sheetPanel === "discovery"
          ? <Button kind="main" size="lg" block aria-pressed={discoveryKept} aria-busy={busy || undefined} unavailable={discoveryKept ? "Kept in your fieldbook." : undefined}
              onClick={() => { if (!busy && !discoveryKept) void execute({ action: "keep", id: discovery as PaperDiscoveryId }); }}>{discoveryKept ? "Kept in your fieldbook" : "Keep this story"}</Button>
          : undefined;

  return (
    <KobraScope
      className={`journey-paper island-views coast tone-pencilatlas jm-frame ${phone ? "jm-frame--phone" : "jm-frame--desk"} ${building ? "is-building" : "is-viewing"}${inPlace ? " is-reading" : ""}`}
    >
      <main className="student-app">
        {phone ? (
          <div className="jm-head">
            <PageHeader onBack={onBack} title="My Island" className="jm-place" actions={<>{welcome}{points}</>} />
            <div className="jm-segrow">{bar}</div>
          </div>
        ) : (
          <>
            <h1 className="sr-only">My Island</h1>
            <TopBar className="jm-deskbar" lead={welcome} center={bar} action={points} />
          </>
        )}
        <div className="coast-world">
          <div className="coast-map-area">
            {classmate ? (
              <ClassmateIsland
                key={classmate.uid}
                classmate={classmate}
                cohort={cohort}
                onBack={() => setClassmate(null)}
                onOpenYear={() => setPanel("year")}
              />
            ) : island ? (
              <IslandMap
                world={world}
                building={building}
                chosen={chosen}
                chosenWonder={chosenWonder}
                candidate={candidate}
                onCandidate={pickCorner}
                editable={editable}
                selectedTile={editing}
                onSelectTile={selectTile}
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
                  <Button kind="main" onClick={() => void execute({ action: "open" })}>Try again</Button>
                )}
              </div>
            )}
            {!classmate && (notice || error) && (
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
                  <IconButton label="Dismiss update" onClick={() => setNotice(null)}
                    icon={<X className="ui-icon" width={20} height={20} strokeWidth={1.75} aria-hidden="true" />} />
                )}
              </div>
            )}
          </div>
          <BuildDrawer open={building} title={editing ? "Make room for something new." : "A little more of your world."}>
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
            {editor ? (
              <TileEditor
                name={tileName(editor.tile)}
                replaceName={chosenWonder ? crewById[chosenWonder].wonder : selected.name}
                replaceNote={editor.replaceNote}
                replaceBlock={editor.replaceBlock}
                removeNote={editor.removeNote}
                removeBlock={editor.removeBlock}
                note={editor.note}
                busy={busy}
                onReplace={() => void replaceTile()}
                onUndo={() => void undo()}
                canUndo={!!world.history.length}
                onRemove={() => void removeTile()}
                onClose={() => setEditing(null)}
              />
            ) : (
              <Placement
                world={world}
                chosen={chosen}
                chosenWonder={chosenWonder}
                candidate={candidate}
                onPlace={() => void build()}
                onUndo={() => void undo()}
                busy={busy}
              />
            )}
          </BuildDrawer>
          {inPlace && (
            <section className="jm-page" aria-label={section === "fieldbook" ? "Your fieldbook" : "Your year"}>
              <div className="jm-page-col">
                {section === "year" && (
                  <YearIslandsBook
                    cohort={cohort}
                    school={yearSchool ? getSchoolName(yearSchool) : ""}
                    status={year.status}
                    classmates={year.classmates}
                    visibility={year.visibility}
                    visibilityKnown={year.visibilityKnown}
                    visibilityError={year.visibilityError}
                    onVisibility={year.setVisibility}
                    onVisit={visitClassmate}
                    onRetry={year.reload}
                    onOpenSetup={onOpenSetup ? () => { setPanel(null); onOpenSetup(); } : undefined}
                    sample={year.sample}
                  />
                )}
                {section === "fieldbook" && (
                  <>
                    <SelectionWords<"stories" | "visitors" | "wonders"> label="Fieldbook sections" value={fieldbookSection} onChange={setFieldbookSection} className="jm-fb-words"
                      options={[{ value: "stories", label: "Stories" }, { value: "visitors", label: "Visitors" }, { value: "wonders", label: "Wonder tiles" }]} />
                    {fieldbookSection === "stories" && (
                      <div className="fieldbook-panel jm-fb">
                        <div className="jm-fb-head">
                          <p className="t-label jm-label">Your field notes</p>
                          <h2 className="t-title jm-fb-title">Things found<br /><em className="jm-live">along the way.</em></h2>
                        </div>
                        <p className="t-sub">
                          Mythic stickers come into view as your island grows. Choose an
                          undiscovered story below and we’ll point out a corner to build
                          towards it.
                        </p>
                        {kept.length < discoveries.length && (
                          <TextButton arrow="forward" className="jm-find" onClick={() => findSticker()}>Find a sticker</TextButton>
                        )}
                        <List className="fieldbook-discoveries" label="Stories">
                          {discoveries.map((d) => {
                            const visible = seen.some((s) => s.id === d.id);
                            return (
                              <Row
                                key={d.id}
                                forward
                                icon={visible ? undefined : <Compass className="ui-icon" width={24} height={24} strokeWidth={1.75} aria-hidden="true" />}
                                art={visible ? <StickerArt id={d.id} /> : undefined}
                                title={visible ? legendById[d.id].name : "Somewhere in the mist"}
                                meta={visible ? kept.includes(d.id) ? "Kept in your fieldbook" : "In sight · take a closer look" : "Show me the way"}
                                onPress={() => visible ? showDiscovery(d.id) : findSticker(d.id)}
                              />
                            );
                          })}
                        </List>
                      </div>
                    )}
                    {island&&fieldbookSection==="visitors"&&<VisitorsBook island={island} onVisit={openVisitor}/>}
                    {island&&fieldbookSection==="wonders"&&<WondersBook island={island} onWonder={id=>openVisitor(id,"wonder")}/>}
                  </>
                )}
              </div>
            </section>
          )}
        </div>
      </main>
      <Sheet open={sheetPanel !== null} onClose={() => setPanel(null)} title={sheetTitle} titleSize="small" hideTitle={sheetPanel !== "visitor"}
        className={`island-sheet jm-sheet${sheetPanel === "visitor" ? " has-visitor" : ""}`} footer={sheetFooter}>
        <ScrollTop marker={`${sheetPanel}:${visitor}:${visitorPage}:${inspected}:${discovery}:${treasure}`} />
        <div className="journey-paper jm-sheet-inner">
        {sheetPanel==="visitor"&&island&&<VisitorPanel id={visitor} page={visitorPage} island={island} busy={busy} error={error} onPage={setVisitorPage} onClose={()=>setPanel(null)} onBuildAnchor={()=>buildVisitorWish(visitor,true)} onBuildWish={()=>buildVisitorWish(visitor)} onPlaceWonder={()=>chooseWonder(visitor)}
          onMeet={()=>void execute({action:"meetVisitor",id:visitor})}
          onClaim={()=>{const id=visitor;void execute({action:"claimVisitor",id}).then(saved=>{if(saved&&currentVisitor.current===id&&currentPanel.current==="visitor")setVisitorPage("gift");});}}
        />}
        {sheetPanel === "points" && (
          <div className="points-panel jm-sheet-copy">
            <p className="t-label jm-label">Your Journey Points</p>
            <h2 className="t-title">A little study.<br />A little more world.</h2>
            <p className="jm-big"><span>{balance.toLocaleString()}</span><small> JP</small></p>
            <p className="t-sub">
              Earn points as you study, then choose what to add to your
              island. There’s no upkeep to pay. New ranks give you three
              meadow tiles to place wherever you like.
            </p>
            <dl className="jm-facts">
              <div><dt>In your pocket</dt><dd className="ui-readout">{balance} JP</dd></div>
              <div><dt>Spent on this island</dt><dd className="ui-readout">{world.log.reduce((sum, item) => sum + item.cost, 0)} JP</dd></div>
              <div><dt>Meadow tiles earned</dt><dd className="ui-readout">{world.credits}</dd></div>
            </dl>
          </div>
        )}
        {sheetPanel === "tile" && (
          <div className="tile-detail-panel jm-sheet-copy">
            <TilePortrait kind={inspected} />
            <p className="t-label jm-label">Part of your world</p>
            <h2 className="t-title">{tileById[inspected].name}</h2>
            <p className="t-sub">{tileById[inspected].description}</p>
          </div>
        )}
        {sheetPanel === "treasure" && (
          <div className="tile-detail-panel jm-sheet-copy">
            <TilePortrait kind="treasure" />
            <p className="t-label jm-label">Off the beaten path</p>
            <h2 className="t-title">{PAPER_LANDMARKS.find((d) => d.id === treasure)?.name}</h2>
            <p className="t-sub">
              Someone left a little room to grow. Open this chest to collect
              two meadow tiles. Opening a chest keeps the path you built to
              reach it.
            </p>
          </div>
        )}
        {sheetPanel === "discovery" && (
          <div className="discovery-detail-panel jm-sheet-copy">
            <div className="jm-discovery-art" style={{ backgroundImage: `url(${coastalMap})` }}>
              <StickerArt id={discovery} />
            </div>
            <p className="t-label jm-label">A little something, found</p>
            <h2 className="t-title">{legendById[discovery].name}</h2>
            <p className="t-sub">{legendById[discovery].story}</p>
          </div>
        )}
        </div>
      </Sheet>
    </KobraScope>
  );
}

/** A sheet opens at its top whenever what it shows changes (today's Overlay did the same). */
function ScrollTop({ marker }: { marker: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  useLayoutEffect(() => {
    const body = ref.current?.closest(".ui-sheet-body");
    if (body) body.scrollTop = 0;
  }, [marker]);
  return <span ref={ref} hidden />;
}

import React, { useMemo, useState } from "react";
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
  type ShelfGroup,
} from "./paper/model";
import { coastalMap, legendById, type LegendId } from "./paper/collection";
import { StickerArt } from "./paper/StickerArt";
import { TilePortrait } from "./paper/TileArt";
import "./paper/paper.css";

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
export default function JourneyView({ user, onBack, hasSeenWelcome, onDismissWelcome }: JourneyViewProps) {
  const { island, balance, busy, error, execute } = usePaperIsland(user.uid);
  const [building, setBuilding] = useState(false),
    [chosen, setChosen] = useState<TileKind>("meadow"),
    [candidate, setCandidate] = useState<string | null>(null),
    [camera, setCamera] = useState(defaultCamera),
    [group, setGroup] = useState<ShelfGroup>("All tiles"),
    [notice, setNotice] = useState("");
  const [panel, setPanel] = useState<
      "fieldbook" | "points" | "tile" | "discovery" | "treasure" | null
    >(null),
    [inspected, setInspected] = useState<TileKind>("meadow"),
    [discovery, setDiscovery] = useState<LegendId>("lantern-nautilus");
  const [treasure, setTreasure] = useState("");
  const placed = useMemo(
    () =>
      island
        ? [
            ...island.tiles.map((t) => piece(t.q, t.r, t.kind, t.edge)),
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
          .map((t) => ({ kind: t.kind, cost: t.cost })) ?? [],
    }),
    [placed, balance, island],
  );
  const seen = visibleDiscoveries(placed),
    selected = tileById[chosen],
    kept = island?.kept ?? [];
  const changeMode = (value: boolean) => {
    setBuilding(value);
    setCandidate(null);
    setNotice("");
  };
  const choose = (kind: TileKind) => {
    setChosen(kind);
    setNotice("");
  };
  const build = async () => {
    if (!candidate || !island) return;
    const [q, r] = candidate.split(",").map(Number);
    if (
      await execute({
        action: "place",
        kind: chosen,
        q,
        r,
        requestId: crypto.randomUUID(),
        revision: island.revision,
      })
    ) {
      setCandidate(null);
      const found = visibleDiscoveries([...placed, piece(q, r, chosen)])
        .find(d => !seen.some(previous => previous.id === d.id));
      if (found) {
        setNotice("");
        showDiscovery(found.id);
      } else {
        setNotice(`${selected.name} added. A little more of the map is yours to explore.`);
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
      setNotice("Last tile returned, along with its points or earned tile.");
    }
  };
  const showDiscovery = (id: LegendId) => {
    setDiscovery(id);
    setPanel("discovery");
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
    setGroup("All tiles");
    setCandidate(next.key);
    setCamera({ x: next.x, y: next.y - 75, zoom: 1 });
    setNotice(route.path.length === 1
      ? "Place a tile in the highlighted corner to uncover a mythic sticker."
      : `Start at the highlighted corner. A mythic sticker is ${route.path.length} placements away along this route.`);
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
                candidate={candidate}
                onCandidate={setCandidate}
                onInspect={(kind) => {
                  setInspected(kind);
                  setPanel("tile");
                }}
                onDiscover={showDiscovery}
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
                <button
                  className="primary-action"
                  onClick={() => changeMode(true)}
                >
                  <Hammer size={17} /> Build your island
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
          </div>
          <div
            className="coast-build-tray"
            inert={!building}
            aria-hidden={!building}
          >
            <TileShelf
              chosen={chosen}
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
              candidate={candidate}
              onPlace={() => void build()}
              onUndo={() => void undo()}
              busy={busy}
            />
          </div>
        </div>
      </main>
      {(notice || error) && (
        <div className="island-notice" role={error ? "alert" : "status"}>
          <span>{error || notice}</span>
          {!error && (
            <button aria-label="Dismiss update" onClick={() => setNotice("")}>
              <X size={14} />
            </button>
          )}
        </div>
      )}
      {panel && (
        <Overlay
          title={
            panel === "fieldbook"
              ? "Your fieldbook"
              : panel === "points"
                ? "Your Journey Points"
                : panel === "tile"
                  ? tileById[inspected].name
                  : panel === "treasure"
                    ? "A treasure, found"
                    : legendById[discovery].name
          }
          onClose={() => setPanel(null)}
        >
          {panel === "fieldbook" && (
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
            </div>
          )}
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

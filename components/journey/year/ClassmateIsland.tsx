/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */
import React, { useMemo, useState } from 'react';
import { ArrowLeft, Users } from 'lucide-react';
import Avatar from '../../Avatar';
import { IslandMap, Overlay, defaultCamera } from '../paper/MapControls';
import { TilePortrait } from '../paper/TileArt';
import { StickerArt } from '../paper/StickerArt';
import { coastalMap, legendById, type LegendId } from '../paper/collection';
import { tileById, type TileKind } from '../paper/catalogue';
import { crewById, type CrewId } from '../visitors/catalogue';
import { WonderTileArt } from '../visitors/VisitorArt';
import { PAPER_LANDMARKS } from '../../../functions/src/paperIslandModel';
import { islandPieces, possessive, readOnlyWorld, type YearIsland } from './yearIslands';

type Panel =
  | { type: 'tile'; kind: TileKind; landmark?: string }
  | { type: 'discovery'; id: LegendId }
  | { type: 'wonder'; id: CrewId };

const noop = () => {};

/**
 * A classmate's island, look only. The same renderer and pan layer as the
 * student's own island, with nothing that builds, buys, keeps or claims: the
 * world has no balance and no open corners, and every panel only describes.
 */
export function ClassmateIsland({ classmate, cohort, onBack, onOpenYear }: {
  classmate: YearIsland;
  /** "5th Year at Marino" */
  cohort: string;
  onBack: () => void;
  onOpenYear: () => void;
}) {
  const [camera, setCamera] = useState(defaultCamera);
  const [panel, setPanel] = useState<Panel | null>(null);
  const world = useMemo(() => readOnlyWorld(islandPieces(classmate.tiles)), [classmate.tiles]);
  const owner = possessive(classmate.name);
  const tiles = `${classmate.tileCount} ${classmate.tileCount === 1 ? 'tile' : 'tiles'}`;
  const title = !panel ? '' : panel.type === 'tile'
    ? panel.landmark ? PAPER_LANDMARKS.find(l => l.id === panel.landmark)?.name ?? tileById[panel.kind].name : tileById[panel.kind].name
    : panel.type === 'wonder' ? crewById[panel.id].wonder : legendById[panel.id].name;
  return (
    <>
      <IslandMap
        world={world}
        building={false}
        chosen="meadow"
        candidate={null}
        onCandidate={noop}
        onInspect={kind => setPanel({ type: 'tile', kind })}
        onDiscover={id => setPanel({ type: 'discovery', id })}
        onTreasure={id => setPanel({ type: 'tile', kind: 'treasure', landmark: id })}
        onInspectWonder={id => setPanel({ type: 'wonder', id })}
        camera={camera}
        setCamera={setCamera}
        label={`${owner} island, look only. Drag to explore or use the arrow keys to pan.`}
      />
      <div className="visit-banner" data-visiting={classmate.uid}>
        <span className="visit-banner-avatar"><Avatar seed={classmate.avatar} alt="" /></span>
        <span className="visit-banner-copy">
          <small>Visiting · look only</small>
          <strong>{owner} island</strong>
          <span>{cohort ? `${cohort} · ${tiles}` : tiles}</span>
        </span>
      </div>
      <div className="island-dock visit-dock">
        <button type="button" onClick={onOpenYear}>
          <Users size={18} />
          <span>Your year</span>
        </button>
        <button type="button" className="primary-action" onClick={onBack}>
          <ArrowLeft size={17} />
          <span>Back to your island</span>
        </button>
      </div>
      {panel && (
        <Overlay title={title} onClose={() => setPanel(null)} scrollKey={JSON.stringify(panel)}>
          {panel.type === 'tile' && (
            <div className="tile-detail-panel">
              <TilePortrait kind={panel.kind} />
              <span className="eyebrow">ON {owner.toUpperCase()} ISLAND</span>
              <h2>{title}</h2>
              <p>{panel.landmark
                ? `${classmate.name} built far enough across the map to reach this place.`
                : tileById[panel.kind].description}</p>
            </div>
          )}
          {panel.type === 'wonder' && (
            <div className="tile-detail-panel">
              <WonderTileArt id={panel.id} className="tile-portrait" />
              <span className="eyebrow">A GIFT FROM {crewById[panel.id].name.toUpperCase()}</span>
              <h2>{title}</h2>
              <p>{crewById[panel.id].wonderStory}</p>
            </div>
          )}
          {panel.type === 'discovery' && (
            <div className="discovery-detail-panel">
              <div style={{ backgroundImage: `url(${coastalMap})` }}>
                <StickerArt id={panel.id} />
              </div>
              <section>
                <span className="eyebrow">IN SIGHT OF {owner.toUpperCase()} ISLAND</span>
                <h2>{title}</h2>
                <p>{legendById[panel.id].story}</p>
              </section>
            </div>
          )}
        </Overlay>
      )}
    </>
  );
}

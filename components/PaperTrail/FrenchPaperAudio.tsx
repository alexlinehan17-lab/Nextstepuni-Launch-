import AudioSourcePlayer from '../MarkBank/AudioSourcePlayer';
import type { CardAudioMaterial } from '../../types/markBank';

/** The paper's recording, shared by the Atlas crop and full document viewer: Mark Bank's player
 *  on the page's own surface, so it follows the theme. */
export default function FrenchPaperAudio({ source }: { source: CardAudioMaterial }) {
  return <div className="pt-recording">
    <AudioSourcePlayer source={source} />
  </div>;
}

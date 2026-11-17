import { Composition } from 'remotion';
import { Main } from './Main';
import { TOTAL } from './timeline';

export const Root: React.FC = () => (
  <Composition
    id="ShotcraftLab"
    component={Main}
    durationInFrames={TOTAL}
    fps={30}
    width={960}
    height={540}
  />
);

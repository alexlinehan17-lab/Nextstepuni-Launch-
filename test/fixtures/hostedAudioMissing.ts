/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 *
 * SEC recordings and videos that live cards (or the Topic Atlas) play and that
 * have no verified copy in Firebase Storage yet. Until one has a copy, its
 * cards play the SEC's own address, as before.
 *
 * This list only shrinks. A recording comes off it in the same change that
 * uploads it (scripts/markbank/audio-hosting/host_audio.py extends
 * audio-manifest.json and components/MarkBank/hostedAudio.json); a card whose
 * recording is neither hosted nor listed here fails
 * test/markBankHostedAudio.test.tsx. Entries may be added only by a
 * coordinator ruling recorded beside them; otherwise upload the recording,
 * never add to this list to make that test pass.
 */
export const HOSTED_AUDIO_MISSING: readonly string[] = [
  'audio/2010/LC001ZLP017IV.mp3',
  'audio/2010/LC012ZLP017EV.mp3',
  'audio/2010/LC058ZLP017EV.mp3',
  'audio/2010/LC099ZLP017EV.mp3',
  'audio/2011/LC001BLP017IV.mp3',
  'audio/2011/LC001ZLP017IV.mp3',
  'audio/2011/LC011ZLP017EV.mp3',
  'audio/2011/LC012ZLP017EV.mp3',
  'audio/2011/LC058ZLP017EV.mp3',
  'audio/2011/LC099ZLP017EV.mp3',
  'audio/2012/LC001BLPO17IV.mp3',
  'audio/2012/LC001ZLPO17IV.mp3',
  'audio/2012/LC012ZLPO17EV.mp3',
  'audio/2012/LC058ZLPO17EV.mp3',
  'audio/2012/LC099ZLPO17EV.mp3',
  'audio/2013/LC001BLP017IV.mp3',
  'audio/2013/LC001ZLP017IV.mp3',
  'audio/2013/LC011ZLP017EV.mp3',
  'audio/2013/LC012ZLP017EV.mp3',
  'audio/2013/LC058ZLP017EV.mp3',
  'audio/2013/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2013/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2013/LC099ZLP017EV.mp3',
  'audio/2014/LC001BLP017IV.mp3',
  'audio/2014/LC001ZLP017IV.mp3',
  'audio/2014/LC011ZLP017EV.mp3',
  'audio/2014/LC012ZLP017EV.mp3',
  'audio/2014/LC058ZLP017EV.mp3',
  'audio/2014/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2014/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2014/LC099ZLP017EV.mp3',
  'audio/2015/LC001BLP017IV.mp3',
  'audio/2015/LC001ZLP017IV.mp3',
  'audio/2015/LC011ZLP017EV.mp3',
  'audio/2015/LC012ZLP017EV.mp3',
  'audio/2015/LC058ZLP017EV.mp3',
  'audio/2015/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2015/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2015/LC099ZLP017EV.mp3',
  'audio/2016/LC001BLP017IV.mp3',
  'audio/2016/LC001ZLP017IV.mp3',
  'audio/2016/LC011ZLP017EV.mp3',
  'audio/2016/LC012ZLP017EV.mp3',
  'audio/2016/LC058ZLP017EV.mp3',
  'audio/2016/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2016/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2016/LC099ZLP017EV.mp3',
  'audio/2017/LC001BLP017IV.mp3',
  'audio/2017/LC001ZLP017IV.mp3',
  'audio/2017/LC011ZLP017EV.mp3',
  'audio/2017/LC012ZLP017EV.mp3',
  'audio/2017/LC058ZLP017EV.mp3',
  'audio/2017/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2017/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2018/LC001BLP017IV.mp3',
  'audio/2018/LC001ZLP017IV.mp3',
  'audio/2018/LC011ZLP017EV.mp3',
  'audio/2018/LC012ZLP017EV.mp3',
  'audio/2018/LC058ZLP017EV.mp3',
  'audio/2018/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2018/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2018/LC099ZLP017EV.mp3',
  'audio/2019/LC001BLP017IV.mp3',
  'audio/2019/LC001ZLP017IV.mp3',
  'audio/2019/LC011ZLP017EV.mp3',
  'audio/2019/LC012ZLP017EV.mp3',
  'audio/2019/LC058ZLP017EV.mp3',
  'audio/2019/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2019/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2019/LC099ZLP017EV.mp3',
  'audio/2020/LC001BLP017IV.mp3',
  'audio/2020/LC001ZLP017IV.mp3',
  'audio/2020/LC011ZLP017EV.mp3',
  'audio/2020/LC012ZLP017EV.mp3',
  'audio/2020/LC058ZLP017EV.mp3',
  'audio/2020/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2020/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2020/LC099ZLP017EV.mp3',
  'audio/2021/LC001BLP017IV.mp3',
  'audio/2021/LC001ZLP017IV.mp3',
  'audio/2021/LC011ZLP017EV.mp3',
  'audio/2021/LC012ZLP017EV.mp3',
  'audio/2021/LC058ZLP017EV.mp3',
  'audio/2021/LC067ZLP117EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2021/LC067ZLP217EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2021/LC099ZLP017EV.mp3',
  'audio/2022/LC001BLP017IV.mp3',
  'audio/2022/LC001ZLP017IV-deferred.mp3',
  'audio/2022/LC001ZLP017IV.mp3',
  'audio/2022/LC011CLP017BV-deferred.mp3',
  'audio/2022/LC011CLP017BV.mp3',
  'audio/2022/LC012ZLP017BV-deferred.mp3',
  'audio/2022/LC012ZLP017BV.mp3',
  'audio/2022/LC058ZLP017BV.mp3',
  'audio/2022/LC067ZLP045EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2022/LC067ZLP046EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2022/LC099ZLP017BV.mp3',
  'audio/2022/LC548ZLP017BV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2023/LC001BLP017IV.mp3',
  'audio/2023/LC001ZLP017IV-deferred.mp3',
  'audio/2023/LC001ZLP017IV.mp3',
  'audio/2023/LC011CLP017BV.mp3',
  'audio/2023/LC012ZLP017BV.mp3',
  'audio/2023/LC058ZLP017BV.mp3',
  'audio/2023/LC067ZLP045EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2023/LC067ZLP046EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2023/LC099ZLP017BV.mp3',
  'audio/2023/LC548ZLP017BV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2024/LC001BLP017IV.mp3',
  'audio/2024/LC001ZLP017IV-deferred.mp3',
  'audio/2024/LC001ZLP017IV.mp3',
  'audio/2024/LC011CLP017BV.mp3',
  'audio/2024/LC012ZLP017BV.mp3',
  'audio/2024/LC058ZLP017BV.mp3',
  'audio/2024/LC067ZLP045EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2024/LC067ZLP046EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2024/LC099ZLP017BV.mp3',
  'audio/2024/LC548ZLP017BV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2025/LC001BLP017IV.mp3',
  'audio/2025/LC001ZLP017IV-deferred.mp3',
  'audio/2025/LC001ZLP017IV.mp3',
  'audio/2025/LC011CLP017BV.mp3',
  'audio/2025/LC012ZLP017BV.mp3',
  'audio/2025/LC067ZLP045EV.mp3',
  'audio/2025/LC067ZLP046EV.mp3',
  'audio/2025/LC548ZLP017BV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2026/LC001BLP017IV.mp3',
  'audio/2026/LC001ZLP017IV.mp3',
  'audio/2026/LC011CLP017BV.mp3',
  'audio/2026/LC012ZLP017BV.mp3',
  'audio/2026/LC067ZLP045EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2026/LC067ZLP046EV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'audio/2026/LC548ZLP017BV.mp3', // Recorded exception, coordinator ruling 19 Nov 2026: the SEC archive has blocked this Mac since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2015/LC462CLPO31EV.mp4', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2016/LC462CLP031EV.mp4', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2017/LC462CLP031EV.mp4', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2018/LC462CLP031EV.mp4', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2019/LC462CLP031EV.mp4', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2020/LC462CLP031EV.mp4', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2021/LC462CLP031EV.mov', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2022/LC462CLP031EV.mov', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2023/LC462CLP031EV.mov', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2024/LC462CLP031EV.mov', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2025/LC462CLP031EV.mov', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  'video/2026/LC462CLP031EV.mov', // Recorded exception, coordinator ruling 19 Nov 2026: LCVP Link Modules video (#374), SEC archive blocked since 19 Nov 11:19 UTC; owner: audio-hosting lane.
  // Recorded exception (coordinator ruling 19 Nov): Italian listening recordings
  // carded on claude/classics-lane-20261118. Not uploaded because the SEC
  // archive has been blocking this Mac since 19 Nov 11:19 UTC; owner: the
  // audio-hosting lane, which fetches and uploads these first when the block
  // lifts and takes them off this list. Fingerprints: data/italianAudio.json,
  // whose 2010-2020 entries the Topic Atlas lists as well.
  'audio/2010/LC013ZLP017EV.mp3',
  'audio/2011/LC013ZLP017EV.mp3',
  'audio/2012/LC013ZLPO17EV.mp3',
  'audio/2013/LC013ZLP017EV.mp3',
  'audio/2014/LC013ZLP017EV.mp3',
  'audio/2015/LC013ZLP017EV.mp3',
  'audio/2016/LC013ZLP017EV.mp3',
  'audio/2017/LC013ZLP017EV.mp3',
  'audio/2018/LC013ZLP017EV.mp3',
  'audio/2019/LC013ZLP017EV.mp3',
  'audio/2020/LC013ZLP017EV.mp3',
  'audio/2021/LC013ZLP017EV.mp3',
  'audio/2022/LC013ZLP017BV.mp3',
  'audio/2023/LC013ZLP017BV.mp3',
  'audio/2024/LC013ZLP017BV.mp3',
  'audio/2025/LC013ZLP017BV.mp3',
];

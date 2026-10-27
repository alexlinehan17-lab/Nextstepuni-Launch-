/**
 * Dev-only "Now" pane for the Kobra review (27 Oct 2026): the REAL Mark Bank
 * session screen, mounted the way MarkBank.tsx mounts it (paperLayout, inside
 * its own Kobra Dialog), on a real card loaded with the bank's own loader.
 *
 * The card is Agricultural Science 2012 HL Q2(b): it has an answer route
 * (Sandy / Clay / Loam) and four priced marking points, so the route chooser,
 * the claim rows, the tally and the three grade buttons all show.
 *
 * So the pane opens "with the answer revealed", the harness clicks the real
 * buttons once the card is on screen: the Sandy route, then Reveal, then the
 * first two marking points. Nothing is faked; every state is the component's.
 *   ?screen=mark-bank-session&state=question   stops before the clicks.
 *   ?screen=mark-bank-session&card=criteria    mounts a Construction Studies
 *     card (2016 HL Q9(a)) whose scheme prices each criterion 0-4, to show the
 *     mark-value picker.
 * Grading or leaving starts the same session again; nothing is stored.
 */
import { useEffect, useState } from 'react';
import SessionScreen from '../../components/MarkBank/SessionScreen';
import { loadCards } from '../../components/MarkBank/deck';
import type { SecCard } from '../../types/markBank';

const params = new URLSearchParams(window.location.search);
const CRITERIA = params.get('card') === 'criteria';
const STOP_AT_QUESTION = params.get('state') === 'question';

const DECK = CRITERIA
  ? { subjectId: 'construction-studies', title: 'Construction Studies', cardId: 'cons-2016-hl-q9-a', route: null }
  : { subjectId: 'agricultural-science', title: 'Agricultural Science', cardId: 'agsci-2012-hl-q2b', route: 'Sandy' };

const buttonWithText = (root: ParentNode, text: string) =>
  Array.from(root.querySelectorAll<HTMLButtonElement>('button')).find(button => button.textContent?.trim() === text);

/** Click through to the revealed scheme with the real controls. Polls, because
 *  the session lives in a portalled Dialog and its rows rise in one by one. */
function useRevealedOnArrival(enabled: boolean, mountKey: number) {
  useEffect(() => {
    if (!enabled || STOP_AT_QUESTION) return;
    let step = DECK.route ? 'route' : 'reveal';
    let tries = 0;
    const timer = window.setInterval(() => {
      tries += 1;
      if (tries > 80) { window.clearInterval(timer); return; }
      const dialog = document.querySelector('.mb-live-session-dialog');
      if (!dialog) return;
      if (step === 'route') {
        const route = buttonWithText(dialog, DECK.route ?? '');
        if (route) { route.click(); step = 'reveal'; }
        return;
      }
      if (step === 'reveal') {
        const reveal = buttonWithText(dialog, 'Reveal the marking scheme');
        if (reveal && !reveal.disabled) { reveal.click(); step = 'claim'; }
        return;
      }
      const pane = dialog.querySelector('.mb-scheme-pane');
      const rows = pane ? Array.from(pane.querySelectorAll<HTMLButtonElement>('button[aria-pressed="false"]')) : [];
      if (!rows.length) return;
      if (CRITERIA) {
        // Award 3 of 4 on the first criterion, so the picker shows a chosen value.
        pane?.querySelector<HTMLButtonElement>('button[aria-label^="Award 3 marks"]')?.click();
      } else {
        rows.slice(0, 2).forEach(row => row.click());
      }
      // Bring the scheme's instruction and rows into view inside the dialog's own scroller.
      window.clearInterval(timer);
      window.setTimeout(() => {
        const workspace = dialog.querySelector<HTMLElement>('.mb-session-workspace');
        const first = rows[0];
        if (!workspace || !first) return;
        workspace.scrollTop += first.getBoundingClientRect().top - workspace.getBoundingClientRect().top - 130;
      }, 400);
    }, 150);
    return () => window.clearInterval(timer);
  }, [enabled, mountKey]);
}

export default function MarkBankSessionBefore() {
  const [deck, setDeck] = useState<SecCard[] | null>(null);
  const [failed, setFailed] = useState(false);
  const [mountKey, setMountKey] = useState(0);
  useEffect(() => {
    let cancelled = false;
    loadCards(DECK.subjectId, 'higher')
      .then(cards => { if (!cancelled) setDeck(cards); })
      .catch(() => { if (!cancelled) setFailed(true); });
    return () => { cancelled = true; };
  }, []);
  const card = deck?.find(item => item.id === DECK.cardId);
  useRevealedOnArrival(Boolean(card), mountKey);

  if (failed) return <p style={{ padding: 24, fontFamily: 'DM Sans, sans-serif' }}>The {DECK.title} deck could not be loaded.</p>;
  if (!deck) return <p style={{ padding: 24, fontFamily: 'DM Sans, sans-serif' }}>Loading the {DECK.title} deck…</p>;
  if (!card) return <p style={{ padding: 24, fontFamily: 'DM Sans, sans-serif' }}>Card {DECK.cardId} is not in the deck.</p>;

  const restart = () => setMountKey(value => value + 1);
  return (
    <SessionScreen
      key={mountKey}
      paperLayout
      cards={[card]}
      subjectLabel={DECK.title}
      reviewPoolTotal={deck.length}
      reviewPoolLabel={DECK.title}
      onGrade={() => undefined}
      onExit={restart}
      onFinish={restart}
    />
  );
}

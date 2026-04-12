import fs from 'fs';
import path from 'path';

const DIR = '/Users/alexlinehan/Nextstepuni-Launch-/components';

function transform(filename, componentName, sectionReplacements) {
  const filePath = path.join(DIR, filename);
  let c = fs.readFileSync(filePath, 'utf-8');

  // 1. Add import if missing
  if (!c.includes('useEssentialsMode')) {
    // Find the last 'import' line (the one closest to the const theme = ... line)
    const themeLineIdx = c.indexOf('\nconst theme =');
    if (themeLineIdx === -1) {
      // Find last import
      const lines = c.split('\n');
      let lastIdx = 0;
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].match(/^import /)) lastIdx = i;
      }
      lines.splice(lastIdx + 1, 0, "import { useEssentialsMode } from '../hooks/useEssentialsMode';");
      c = lines.join('\n');
    } else {
      c = c.slice(0, themeLineIdx) + "\nimport { useEssentialsMode } from '../hooks/useEssentialsMode';" + c.slice(themeLineIdx);
    }
  }

  // 2. Add hook call if missing
  if (!c.includes('const essentials = useEssentialsMode()')) {
    const compIdx = c.indexOf(`const ${componentName}`);
    if (compIdx !== -1) {
      const arrowIdx = c.indexOf('=> {', compIdx);
      if (arrowIdx !== -1) {
        const nlIdx = c.indexOf('\n', arrowIdx);
        c = c.slice(0, nlIdx + 1) + '  const essentials = useEssentialsMode();\n' + c.slice(nlIdx + 1);
      }
    }
  }

  // 3. Apply section replacements
  for (const [original, replacement] of sectionReplacements) {
    if (c.includes(original)) {
      c = c.replace(original, replacement);
    } else {
      console.warn(`  WARNING: Could not find section text in ${filename}. First 80 chars: "${original.slice(0,80)}..."`);
    }
  }

  fs.writeFileSync(filePath, c);
  console.log(`OK: ${filename}`);
}

// Helper to wrap prose in essentials conditional
function ess(essentialsText, originalText) {
  return `{essentials ? (<>\n${essentialsText}\n</>) : (<>\n${originalText}\n</>)}`;
}

// ==========================================
// 3. TheCognitiveArchitectureModule.tsx (6 sections)
// ==========================================
transform('TheCognitiveArchitectureModule.tsx', 'TheCognitiveArchitectureModule', [
  // S0
  [`<p>To do well in the Leaving Cert, it really helps to understand how the machine you're working with — your own brain — actually handles information. The simplest way to think about it is that your memory has <Highlight description="A simple way of understanding memory: it comes in three stages — a quick flash, a short holding space, and a long-term store." theme={theme}>three stages</Highlight>.</p>
              <p>First, there's <Highlight description="The very first stage of memory — a split-second snapshot of what you see or hear. If you don't pay attention to it, it's gone instantly." theme={theme}>Sensory Memory</Highlight>, the brief flash of what you see or hear. Anything you don't pay attention to here is gone forever. If you <em>do</em> pay attention, it moves to <Highlight description="Your brain's temporary holding space. It can only hold a small amount of information for a short time — think of it as your mental workbench." theme={theme}>Short-Term Memory</Highlight>, your brain's mental workbench. From there, it has to be deliberately moved to <Highlight description="Your brain's permanent storage. This is where knowledge needs to end up if you want to remember it in an exam." theme={theme}>Long-Term Memory</Highlight>, the permanent hard drive. Your entire job as a student is to get better at moving stuff from that workbench into long-term storage.</p>`,
  `{essentials ? (
              <p>Your memory has three stages. <Highlight description="The very first stage of memory — a split-second snapshot of what you see or hear. If you don't pay attention to it, it's gone instantly." theme={theme}>Sensory Memory</Highlight> is a split-second flash. <Highlight description="Your brain's temporary holding space. It can only hold a small amount of information for a short time — think of it as your mental workbench." theme={theme}>Short-Term Memory</Highlight> is your mental workbench. <Highlight description="Your brain's permanent storage. This is where knowledge needs to end up if you want to remember it in an exam." theme={theme}>Long-Term Memory</Highlight> is your hard drive. Your job is to move stuff from the workbench to the hard drive.</p>
              ) : (<>
              <p>To do well in the Leaving Cert, it really helps to understand how the machine you're working with — your own brain — actually handles information. The simplest way to think about it is that your memory has <Highlight description="A simple way of understanding memory: it comes in three stages — a quick flash, a short holding space, and a long-term store." theme={theme}>three stages</Highlight>.</p>
              <p>First, there's <Highlight description="The very first stage of memory — a split-second snapshot of what you see or hear. If you don't pay attention to it, it's gone instantly." theme={theme}>Sensory Memory</Highlight>, the brief flash of what you see or hear. Anything you don't pay attention to here is gone forever. If you <em>do</em> pay attention, it moves to <Highlight description="Your brain's temporary holding space. It can only hold a small amount of information for a short time — think of it as your mental workbench." theme={theme}>Short-Term Memory</Highlight>, your brain's mental workbench. From there, it has to be deliberately moved to <Highlight description="Your brain's permanent storage. This is where knowledge needs to end up if you want to remember it in an exam." theme={theme}>Long-Term Memory</Highlight>, the permanent hard drive. Your entire job as a student is to get better at moving stuff from that workbench into long-term storage.</p>
              </>)}`],
  // S1
  [`<p>Your Short-Term Memory — the part of your brain that <Highlight description="The part of your brain that holds and works with information right now. Think of it as your mental desk — it can only fit a few things on it at once." theme={theme}>holds and works with information right now</Highlight> — is the biggest bottleneck in your learning. It's shockingly limited. You might think you can juggle loads of info, but realistically your brain can only hold about <strong>4 chunks of information</strong> at a time when dealing with complex Leaving Cert material.</p>
              <p>Even worse, without active effort, this information fades in about <strong>15-30 seconds</strong>. This is why you can read a whole page of a textbook and have no memory of it. The information landed on your mental desk but disappeared before it could be saved anywhere. Cramming jams this bottleneck, creating a memory that feels strong but vanishes quickly.</p>`,
  `{essentials ? (
              <p>Your short-term memory holds about 4 things at once. Without effort, they fade in 30 seconds. That is why you can read a page and remember nothing. Cramming jams this bottleneck. The memory feels strong but vanishes fast.</p>
              ) : (<>
              <p>Your Short-Term Memory — the part of your brain that <Highlight description="The part of your brain that holds and works with information right now. Think of it as your mental desk — it can only fit a few things on it at once." theme={theme}>holds and works with information right now</Highlight> — is the biggest bottleneck in your learning. It's shockingly limited. You might think you can juggle loads of info, but realistically your brain can only hold about <strong>4 chunks of information</strong> at a time when dealing with complex Leaving Cert material.</p>
              <p>Even worse, without active effort, this information fades in about <strong>15-30 seconds</strong>. This is why you can read a whole page of a textbook and have no memory of it. The information landed on your mental desk but disappeared before it could be saved anywhere. Cramming jams this bottleneck, creating a memory that feels strong but vanishes quickly.</p>
              </>)}`],
  // S2
  [`<p>Your Long-Term Memory isn't one big box; it's more like a filing cabinet with different drawers for different types of knowledge. Knowing which drawer you're using helps you study smarter.</p>
              <p>The first drawer is <Highlight description="Your store of facts and general knowledge — things like Biology definitions, History dates, or what the capital of France is." theme={theme}>fact memory</Highlight> — your library of facts and definitions. The second is <Highlight description="Your store of personal experiences — like remembering a specific Chemistry experiment or what happened in class last Tuesday." theme={theme}>experience memory</Highlight> — your personal collection of things that happened to you. The third, and most important for many subjects, is <Highlight description="Your store of skills and 'how-to' knowledge — like how to solve a Maths equation or conjugate a French verb. It's muscle memory for your brain." theme={theme}>skill memory</Highlight>. Maths isn't about memorising facts; it's about practising steps until they become automatic.</p>`,
  `{essentials ? (
              <p>Long-term memory has three drawers. <Highlight description="Your store of facts and general knowledge — things like Biology definitions, History dates, or what the capital of France is." theme={theme}>Fact memory</Highlight> stores definitions and dates. <Highlight description="Your store of personal experiences — like remembering a specific Chemistry experiment or what happened in class last Tuesday." theme={theme}>Experience memory</Highlight> stores personal events. <Highlight description="Your store of skills and 'how-to' knowledge — like how to solve a Maths equation or conjugate a French verb. It's muscle memory for your brain." theme={theme}>Skill memory</Highlight> stores how-to knowledge. Match your study method to the drawer you need.</p>
              ) : (<>
              <p>Your Long-Term Memory isn't one big box; it's more like a filing cabinet with different drawers for different types of knowledge. Knowing which drawer you're using helps you study smarter.</p>
              <p>The first drawer is <Highlight description="Your store of facts and general knowledge — things like Biology definitions, History dates, or what the capital of France is." theme={theme}>fact memory</Highlight> — your library of facts and definitions. The second is <Highlight description="Your store of personal experiences — like remembering a specific Chemistry experiment or what happened in class last Tuesday." theme={theme}>experience memory</Highlight> — your personal collection of things that happened to you. The third, and most important for many subjects, is <Highlight description="Your store of skills and 'how-to' knowledge — like how to solve a Maths equation or conjugate a French verb. It's muscle memory for your brain." theme={theme}>skill memory</Highlight>. Maths isn't about memorising facts; it's about practising steps until they become automatic.</p>
              </>)}`],
  // S3
  [`<p>Moving information from your temporary workbench to your permanent hard drive is called <Highlight description="The process of turning a temporary memory into a lasting one. How deeply you think about something decides how well you'll remember it." theme={theme}>encoding</Highlight> — basically, hitting the 'save' button. But not all saving is equal. <Highlight description="When you only skim the surface of something — like re-reading a definition without really thinking about it. This creates weak memories that fade fast." theme={theme}>Surface-level studying</Highlight>, like just re-reading a definition, creates weak, flimsy memories.</p>
              <p><Highlight description="When you really think about what something means and connect it to things you already know. This creates strong memories that last." theme={theme}>Deep studying</Highlight> is about connecting new information to what you already know. For example, learning that "mitochondria is the powerhouse of the cell" is surface-level. Understanding <em>how</em> it produces energy and why that's essential for your muscles to work is deep. What's actually happening in your brain is that <Highlight description="When brain cells fire together repeatedly, the connections between them get physically stronger — like a path getting worn into a field the more you walk it." theme={theme}>the connections between your brain cells get physically stronger</Highlight> — the more you use a pathway, the easier it becomes to use again.</p>`,
  `{essentials ? (
              <p><Highlight description="The process of turning a temporary memory into a lasting one. How deeply you think about something decides how well you'll remember it." theme={theme}>Encoding</Highlight> is how you save memories. Re-reading creates weak saves. Connecting new info to what you already know creates strong saves. The deeper you think, the better you remember.</p>
              ) : (<>
              <p>Moving information from your temporary workbench to your permanent hard drive is called <Highlight description="The process of turning a temporary memory into a lasting one. How deeply you think about something decides how well you'll remember it." theme={theme}>encoding</Highlight> — basically, hitting the 'save' button. But not all saving is equal. <Highlight description="When you only skim the surface of something — like re-reading a definition without really thinking about it. This creates weak memories that fade fast." theme={theme}>Surface-level studying</Highlight>, like just re-reading a definition, creates weak, flimsy memories.</p>
              <p><Highlight description="When you really think about what something means and connect it to things you already know. This creates strong memories that last." theme={theme}>Deep studying</Highlight> is about connecting new information to what you already know. For example, learning that "mitochondria is the powerhouse of the cell" is surface-level. Understanding <em>how</em> it produces energy and why that's essential for your muscles to work is deep. What's actually happening in your brain is that <Highlight description="When brain cells fire together repeatedly, the connections between them get physically stronger — like a path getting worn into a field the more you walk it." theme={theme}>the connections between your brain cells get physically stronger</Highlight> — the more you use a pathway, the easier it becomes to use again.</p>
              </>)}`],
  // S4
  [`<p>Here's something your brain absolutely needs: the final "save" button gets hit while you sleep. During the day, new information sits in a <Highlight`,
  `{essentials ? (
              <p>Your brain saves memories while you sleep. During the day, info sits in a temporary inbox. During deep sleep, your brain moves it to permanent storage. Pulling an all-nighter is self-sabotage. Sleep is not optional.</p>
              ) : (<>
              <p>Here's something your brain absolutely needs: the final "save" button gets hit while you sleep. During the day, new information sits in a <Highlight`],
  // close the S4 conditional
  [`Pulling an all-nighter is like trying to save a file while constantly hitting 'cancel' on the save dialog. It's self-sabotage.</p>`,
  `Pulling an all-nighter is like trying to save a file while constantly hitting 'cancel' on the save dialog. It's self-sabotage.</p>
              </>)}`],
  // S5
  [`<p>Understanding how your memory works gives you an owner's manual for your own brain. It shows that doing well isn't about "natural talent" — it's about using the right approach. Strategies like testing yourself, spacing out your study, and mixing topics are all just ways to work with how your memory naturally operates.</p>
              <p>But even the best strategies will fail if you're running on empty. Your <Highlight description`,
  `{essentials ? (<>
              <p>Doing well is not about talent. It is about using the right approach. Test yourself. Space your study. Mix topics. And look after your body. Stress, poor sleep, and dehydration all block your memory. Self-care is not optional for your grades.</p>
              </>) : (<>
              <p>Understanding how your memory works gives you an owner's manual for your own brain. It shows that doing well isn't about "natural talent" — it's about using the right approach. Strategies like testing yourself, spacing out your study, and mixing topics are all just ways to work with how your memory naturally operates.</p>
              <p>But even the best strategies will fail if you're running on empty. Your <Highlight description`],
  // close S5 conditional
  [`it's one of the most important things you can do for your grades.</p>`,
  `it's one of the most important things you can do for your grades.</p>
              </>)}`],
]);

// ==========================================
// 4. TheCognitiveLoadModule.tsx (5 sections)
// ==========================================
transform('TheCognitiveLoadModule.tsx', 'TheCognitiveLoadModule', [
  // S0 - open
  [`<p>For a long time, scientists thought your <Highlight description="Your short-term memory is like a tiny desk — it can only hold a few things at once before stuff starts falling off." theme={theme}>short-term memory</Highlight> could hold about 7 things at once. But more recent research showed the real number is much smaller: roughly 4 items.`,
  `{essentials ? (<>
              <p>Your brain can juggle about 4 items at once. When you go over, information drops out silently. You do not feel a "full" signal. Re-reading a dense paragraph fails because there is no room left to process meaning. You are reading but not learning.</p>
              </>) : (<>
              <p>For a long time, scientists thought your <Highlight description="Your short-term memory is like a tiny desk — it can only hold a few things at once before stuff starts falling off." theme={theme}>short-term memory</Highlight> could hold about 7 things at once. But more recent research showed the real number is much smaller: roughly 4 items.`],
  // S0 - close
  [`You're reading, but you're not learning. And because the text looks familiar on each re-read, you mistake that familiarity for actual comprehension.</p>
              <PersonalStory name="Niamh" role="6th Year, Galway">`,
  `You're reading, but you're not learning. And because the text looks familiar on each re-read, you mistake that familiarity for actual comprehension.</p>
              </>)}
              <PersonalStory name="Niamh" role="6th Year, Galway">`],
  // S1
  [`<p>Researchers figured out that there are three types of mental load that compete for your brain's limited capacity. Understanding these three types is the key to making every study session count.</p>`,
  `{essentials ? (
              <p>Three types of load compete for your brain. Built-in difficulty is the topic itself. Wasted effort is distractions and bad layouts. Actual learning effort is making sense of ideas. Cut wasted effort so your brain has room for real learning.</p>
              ) : (
              <p>Researchers figured out that there are three types of mental load that compete for your brain's limited capacity. Understanding these three types is the key to making every study session count.</p>
              )}`],
  // S2
  [`<p>One of the sneakiest ways your brain gets overloaded is something called <Highlight description="This happens when a diagram is on one part of the page and the explanation is somewhere else. Your brain wastes energy jumping back and forth instead of actually learning." theme={theme}>split attention</Highlight>. When a diagram and its explanation are in different places`,
  `{essentials ? (<>
              <p>When a diagram is on one part of the page and the text is elsewhere, your brain wastes energy jumping between them. Put labels directly on diagrams. Keep text and images together. Studies show this boosts results by 30-50%.</p>
              </>) : (<>
              <p>One of the sneakiest ways your brain gets overloaded is something called <Highlight description="This happens when a diagram is on one part of the page and the explanation is somewhere else. Your brain wastes energy jumping back and forth instead of actually learning." theme={theme}>split attention</Highlight>. When a diagram and its explanation are in different places`],
  [`Every time you stop your brain from having to jump between two sources, you free it up for the thing that actually matters: understanding.</p>`,
  `Every time you stop your brain from having to jump between two sources, you free it up for the thing that actually matters: understanding.</p>
              </>)}`],
  // S3
  [`<p>Here's something that surprises most people: study techniques that help beginners can actually <em>hurt</em> you once you get better at a topic.`,
  `{essentials ? (<>
              <p>Study methods that help beginners can hurt you once you improve. Worked examples are great when starting out. Once you know the approach, switch to solving problems on your own. The methods that got you to 60% will hold you back from 90%.</p>
              </>) : (<>
              <p>Here's something that surprises most people: study techniques that help beginners can actually <em>hurt</em> you once you get better at a topic.`],
  [`which is exactly why knowing what you actually know (from earlier modules) matters so much here.</p>`,
  `which is exactly why knowing what you actually know (from earlier modules) matters so much here.</p>
              </>)}`],
  // S4
  [`<p>Everything in this module comes down to a simple game plan for managing your mental load while studying. Step one:`,
  `{essentials ? (<>
              <p>Here is your game plan. Cut distractions: phone in another room, clean desk, close extra tabs. Break topics into small chunks. Use freed-up brainpower for real learning: explain things to yourself, connect to what you know, test from memory.</p>
              </>) : (<>
              <p>Everything in this module comes down to a simple game plan for managing your mental load while studying. Step one:`],
  [`These two rules make sure every drop of brainpower goes toward real learning.</p>`,
  `These two rules make sure every drop of brainpower goes toward real learning.</p>
              </>)}`],
]);

console.log('Batch 2 done (CogArch + CogLoad)');

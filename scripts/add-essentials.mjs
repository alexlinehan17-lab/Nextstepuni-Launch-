import fs from 'fs';
import path from 'path';

const COMPONENTS_DIR = '/Users/alexlinehan/Nextstepuni-Launch-/components';

// Each module config: filename, componentName, sections with essentials text replacements
const modules = [
  {
    file: 'StrategicAdvantageModule.tsx',
    component: 'StrategicAdvantageModule',
    lastImportMarker: "import { COMPACT_CALLOUT_PLACEMENTS } from '../northStarData';",
    sections: [
      {
        // Section 0: The Story of You
        original: `<p>You are a storyteller. The most important story you will ever tell is the one you tell yourself about your own life. This is your <Highlight description="The ongoing story you tell yourself about who you are and where your life is going. We all have one -- it shapes how you see your past, your present, and what you think is possible for your future." theme={theme}>Narrative Identity</Highlight>. It's how you make sense of your past, present, and future.</p>
              <p>Society often hands students from tough backgrounds a ready-made story: a tale of deficit and struggle. This is a <Highlight description="When something good happens but then something bad follows, and the bad part takes over the whole story. It is the kind of thinking where one setback makes you feel like nothing will ever work out." theme={theme}>Contamination Script</Highlight>. Resilience is the act of radical authorship: rejecting that story and writing your own, a <Highlight description="When something bad happens but you find a way to turn it into something good -- a lesson, a motivation, a turning point. It is choosing to let the rough patch be the start of a comeback, not the end of the road." theme={theme}>Redemption Script</Highlight> where adversity becomes the source of your strength.</p>
              <PersonalStory name="Alex" role="Founder, NextStepUni">
                <p>I had a contamination script running for years. Lad from Togher, wrong crowds, failed the Junior Cert — it would have been easy to let that be the whole story. But in 4th year I rewrote it. I spent the year reading academic papers, built my own learning system, and went from rock bottom to nearly 600 points and a UCC Scholarship. The story didn't change because the facts changed. The facts were the same. I just chose to write a different next chapter.</p>
              </PersonalStory>`,
        essentials: `<p>You tell yourself a story about your life. That story shapes everything. A <Highlight description="When something good happens but then something bad follows, and the bad part takes over the whole story. It is the kind of thinking where one setback makes you feel like nothing will ever work out." theme={theme}>Contamination Script</Highlight> says setbacks define you. A <Highlight description="When something bad happens but you find a way to turn it into something good -- a lesson, a motivation, a turning point. It is choosing to let the rough patch be the start of a comeback, not the end of the road." theme={theme}>Redemption Script</Highlight> turns hard times into fuel. You get to choose which one you run.</p>`
      },
      {
        // Section 1: The Two Pillars
        original: `<p>Every great story is built on two core themes. The first is <Highlight description="The part of your story that is about you taking charge -- your independence, your effort, and your ability to shape your own future through your own actions." theme={theme}>Agency</Highlight>--the story of the self-reliant hero who overcomes obstacles through their own power. The second is <Highlight description="The part of your story that is about the people around you -- your family, friends, and community, and how those relationships have shaped who you are." theme={theme}>Communion</Highlight>--the story of connection, of being supported by family, friends, and community.</p>
                <p>A story of pure Agency leads to the "Isolated Hero" who burns out. A story of pure Communion leads to passivity. The most resilient narrative identities skillfully weave both: "I worked hard (Agency) to honour the sacrifices of my family (Communion)." Finding this balance is key to a sustainable story of success.</p>`,
        essentials: `<p>Great stories blend two themes. <Highlight description="The part of your story that is about you taking charge -- your independence, your effort, and your ability to shape your own future through your own actions." theme={theme}>Agency</Highlight> is your own effort. <Highlight description="The part of your story that is about the people around you -- your family, friends, and community, and how those relationships have shaped who you are." theme={theme}>Communion</Highlight> is the people who support you. Too much of one breaks the story. Balance them: "I worked hard to honour my family."</p>`
      },
      {
        // Section 2: The Power of Failure
        original: `<p>Your life story is not a continuous film; it's a collection of key scenes. These are your <Highlight description="The key moments in your life that stick with you -- the highs, the lows, and the turning points. These are the scenes that define the story you tell about yourself." theme={theme}>Pivotal Moments</Highlight>. For resilient individuals, the most important pivotal moments are often failures. They are the moments where suffering is transformed into insight.</p>
              <p>The key is to learn the art of <Highlight description="Looking at the same event from a different angle so it means something different to you. Instead of 'I failed,' you think 'I found out exactly what I need to work on.' Same facts, different story." theme={theme}>Reframing</Highlight>. A technique like the "Failure Resume" helps you de-shame failure and see it not as a verdict on your worth, but as valuable data for future success. It's about learning to say, "I didn't suffer for nothing; I suffered to become stronger."</p>`,
        essentials: `<p>Your life is a collection of key scenes. Your failures are the most useful ones. Learn to <Highlight description="Looking at the same event from a different angle so it means something different to you. Instead of 'I failed,' you think 'I found out exactly what I need to work on.' Same facts, different story." theme={theme}>reframe</Highlight> them. "I failed" becomes "I found exactly what to work on." Same facts. Different story.</p>`
      },
      {
        // Section 3: The Advantage of Disadvantage
        original: `<p>What if the things that make your academic journey harder are the very things that are making your learning deeper and more durable? This is the principle of <Highlight description="Study methods that feel harder and slower in the moment but actually help you remember things way better in the long run. The struggle is a feature, not a bug." theme={theme}>Desirable Difficulties</Highlight>. Learning that is "easy" (like re-reading notes) is shallow. Learning that is "hard" (like struggling to solve a problem without help) forces deeper processing and builds stronger neural pathways.</p>
              <p>If you have never had a private tutor, you have been forced to figure things out yourself -- and that is actually one of the most powerful ways to learn. If you have less free time, you have probably had to spread your study out instead of cramming, which is exactly what the research says works best. Not having everything handed to you builds real problem-solving skills. These are not disadvantages -- they are hidden training that students with every resource may never get.</p>`,
        essentials: `<p>What makes your journey harder might be making your learning deeper. <Highlight description="Study methods that feel harder and slower in the moment but actually help you remember things way better in the long run. The struggle is a feature, not a bug." theme={theme}>Desirable difficulties</Highlight> build stronger memory. Figuring things out alone beats being spoon-fed. Spreading study beats cramming. Your challenges are hidden training.</p>`
      },
      {
        // Section 4: Your Redemption Script
        original: `<p>You have the power to be the author of your own story. This module has given you the tools of narrative construction: the ability to turn contamination into redemption, to balance agency with communion, and to reframe difficulty as a desirable advantage. Now it's time to put it into practice.</p>
              <p>The final step is to build your own mini-"Failure Resume." By taking a past failure and actively converting it into an asset, you are practicing the core skill of resilient identity construction. You are forging your own redemption script, turning the lead of your past into the gold of your future.</p>`,
        essentials: `<p>You are the author of your story. Turn contamination into redemption. Balance self-reliance with connection. Reframe difficulty as advantage. Build your own "Failure Resume" below. Turn one past failure into an asset you can use.</p>`
      },
    ]
  },
  {
    file: 'TheAutodidactsEngineModule.tsx',
    component: 'TheAutodidactsEngineModule',
    lastImportMarker: "import { ModuleLayout } from './ModuleLayout';",
    sections: [
      {
        original: `<p>Most study time is wasted. It's spent on what we call <Highlight description="Going through the motions without really thinking -- like re-reading your notes or highlighting a textbook. It feels productive, but you're not actually getting better at anything." theme={theme}>Passive Practice</Highlight>--just going through the motions. This feels productive, but it doesn't build skill. To actually get better, you need <Highlight description="Practising with a clear goal, full focus, and -- this is the key part -- a way to check whether you're getting it right. It's harder, but it's what actually makes you improve." theme={theme}>Focused Practice</Highlight>.</p>
              <p>The key ingredient of focused practice is a good feedback loop -- a way to check your work against the right answer. A great teacher does this for you automatically. But when you're studying alone, you don't have that. The goal of this module is to show you how to become your own teacher by building that feedback into your study sessions.</p>`,
        essentials: `<p>Most study is <Highlight description="Going through the motions without really thinking -- like re-reading your notes or highlighting a textbook. It feels productive, but you're not actually getting better at anything." theme={theme}>passive</Highlight> and wasted. You need <Highlight description="Practising with a clear goal, full focus, and -- this is the key part -- a way to check whether you're getting it right. It's harder, but it's what actually makes you improve." theme={theme}>focused practice</Highlight> with a feedback loop. Check your work against the right answer. This module shows you how to be your own teacher.</p>`
      },
      {
        original: `<p>To build your own feedback loop, you need to follow two rules about how your brain works. First, <Highlight description="Your brain learns best when you actually notice your mistakes. If you just skip past errors, you don't learn from them. You need to compare your work against the correct answer so mistakes are impossible to ignore." theme={theme}>Pay Attention to Your Mistakes</Highlight>: Your brain learns the most when it spots an error. If you just gloss over mistakes, nothing sticks. That's why you need to compare your work against a correct version -- a marking scheme, a worked solution, a model answer -- so mistakes become impossible to ignore.</p>
              <p>Second, <Highlight description="Your brain can only hold a few things at once. If you try to do the work AND check the work at the same time, you'll do both badly. Do them separately instead." theme={theme}>Don't Do Everything at Once</Highlight>: Your brain can only juggle so much at one time. You can't do the work and check the work at the same time -- you'll do both badly. This <Highlight description="When your brain tries to handle two demanding tasks at the same time, both suffer. It's like trying to have two conversations at once -- neither one goes well." theme={theme}>mental overload</Highlight> is why checking your work as you go feels so hard. The fix is simple: use a <Highlight description="A two-step process: first you do the work, then you check the work. Keeping these separate means you can give each one your full attention." theme={theme}>two-step process</Highlight> -- first do the work, then check the work. Keep them separate.</p>`,
        essentials: `<p>Two rules for self-study. First, notice your mistakes. Compare your work to the right answer. Second, do the work and check the work separately. Your brain cannot handle both at once. Do step one, then step two.</p>`
      },
      {
        original: `<p>In Maths, your "stand-in teacher" is a full worked solution or marking scheme. The technique is the <Highlight description="You cover the worked solution, try just the first step yourself, then uncover the first step of the solution to compare. You go one step at a time so you get instant feedback on every single line." theme={theme}>Split-Page Method</Highlight>. You cover the solution, try just one step of the problem, stop, then uncover the correct first step. This gives you instant feedback on every single line of working.</p>
              <p>If your step matches, keep going. If it doesn't -- that's where the real learning happens. Write down in your own words why the correct step was different from yours. This is called <Highlight description="Explaining something to yourself in your own words. It sounds simple, but it forces you to actually understand the 'why' behind each step instead of just copying it." theme={theme}>self-explanation</Highlight> -- and it forces you to actually understand the 'why' behind each step, instead of just copying and moving on.</p>`,
        essentials: `<p>For Maths, use the <Highlight description="You cover the worked solution, try just the first step yourself, then uncover the first step of the solution to compare. You go one step at a time so you get instant feedback on every single line." theme={theme}>Split-Page Method</Highlight>. Cover the solution. Try one step. Uncover and compare. When your answer differs, write down why. That is where real learning happens.</p>`
      },
      {
        original: `<p>For languages, your "stand-in teacher" is a correct text in the language you're learning. The technique is <Highlight description="You translate a passage from Irish (or French, etc.) into English, wait a while, then translate your English version back without looking at the original. Then you compare the two versions side by side to spot your mistakes." theme={theme}>Back-Translation</Highlight>. You take a short passage in Irish (or French, etc.), translate it into English, wait an hour, then translate your English version <em>back</em> into the original language without looking at it. Finally, you compare your version with the original, side by side.</p>
              <p>This is brilliant at exposing <Highlight description="When you accidentally use English grammar or phrasing while writing in another language. For example, structuring an Irish sentence the way you'd say it in English." theme={theme}>English-brain habits</Highlight> -- where you accidentally use English grammar and phrasing while writing in Irish or French. Every difference between your version and the original shows you exactly where your understanding of the language needs work.</p>`,
        essentials: `<p>For languages, use <Highlight description="You translate a passage from Irish (or French, etc.) into English, wait a while, then translate your English version back without looking at the original. Then you compare the two versions side by side to spot your mistakes." theme={theme}>Back-Translation</Highlight>. Translate a passage to English. Wait an hour. Translate it back. Compare with the original. Every difference shows you a gap in your understanding.</p>`
      },
      {
        original: `<p>For essay writing, your "stand-in teacher" is a model essay and the official marking scheme (the PCLM criteria). The technique is the <Highlight description="You go through your own essay four times, each time with a different coloured highlighter, checking one specific thing each time (Purpose, Coherence, Language, Mechanics)." theme={theme}>Four-Highlighter Method</Highlight>. After writing an essay, you go through it four times, each time with a different colour, checking your work against what the examiner is looking for.</p>
                <p>`,
        essentials: `{essentials ? (
                <p>For essays, use the <Highlight description="You go through your own essay four times, each time with a different coloured highlighter, checking one specific thing each time (Purpose, Coherence, Language, Mechanics)." theme={theme}>Four-Highlighter Method</Highlight>. Read your essay four times. Each pass checks one thing: Purpose, Coherence, Language, Mechanics. You get a clear picture of what works and what needs fixing.</p>
                ) : (<><p>For essay writing, your "stand-in teacher" is a model essay and the official marking scheme (the PCLM criteria). The technique is the <Highlight description="You go through your own essay four times, each time with a different coloured highlighter, checking one specific thing each time (Purpose, Coherence, Language, Mechanics)." theme={theme}>Four-Highlighter Method</Highlight>. After writing an essay, you go through it four times, each time with a different colour, checking your work against what the examiner is looking for.</p>
                <p>`
      },
      {
        original: `("Is my essay any good?", you get a clear picture of exactly what's working and what needs fixing.
                </p>`,
        essentials: `("Is my essay any good?", you get a clear picture of exactly what's working and what needs fixing.
                </p></>)}`
      },
      {
        original: `<p>You now have everything you need to study smarter on your own. You've got techniques to turn passive, go-through-the-motions study into focused practice that actually builds skill. You've got the tools to be your own teacher.</p>
              <p>The last step is simple: pick one of these techniques and try it just once this week. You don't need to overhaul your entire study routine overnight. Just take one small step to upgrade how you learn. Pick your mission below.</p>`,
        essentials: `{essentials ? (
              <p>You now have real techniques for solo study. Pick one method from this module. Try it once this week. That is all you need to start.</p>
              ) : (<>
              <p>You now have everything you need to study smarter on your own. You've got techniques to turn passive, go-through-the-motions study into focused practice that actually builds skill. You've got the tools to be your own teacher.</p>
              <p>The last step is simple: pick one of these techniques and try it just once this week. You don't need to overhaul your entire study routine overnight. Just take one small step to upgrade how you learn. Pick your mission below.</p>
              </>)}`
      },
    ]
  },
];

// Process the simple modules first
for (const mod of modules) {
  const filePath = path.join(COMPONENTS_DIR, mod.file);
  let content = fs.readFileSync(filePath, 'utf-8');

  // Add import
  if (!content.includes('useEssentialsMode')) {
    content = content.replace(
      mod.lastImportMarker,
      mod.lastImportMarker + "\nimport { useEssentialsMode } from '../hooks/useEssentialsMode';"
    );
  }

  // Add hook call
  if (!content.includes('const essentials = useEssentialsMode()')) {
    const componentPattern = new RegExp(`(const ${mod.component}[^=]*= \\([^)]*\\) => \\{)`);
    const match = content.match(componentPattern);
    if (match) {
      content = content.replace(componentPattern, '$1\n  const essentials = useEssentialsMode();');
    } else {
      // Try to find it after => {
      const idx = content.indexOf(`const ${mod.component}`);
      if (idx !== -1) {
        const arrowIdx = content.indexOf('=> {', idx);
        if (arrowIdx !== -1) {
          const insertPoint = content.indexOf('\n', arrowIdx) + 1;
          content = content.slice(0, insertPoint) + '  const essentials = useEssentialsMode();\n' + content.slice(insertPoint);
        }
      }
    }
  }

  // Apply section replacements
  for (const section of mod.sections) {
    if (content.includes(section.original)) {
      content = content.replace(
        section.original,
        `{essentials ? (<>${section.essentials}</>) : (<>${section.original}</>)}`
      );
    } else {
      // If it's already a raw replacement (not wrapped)
      content = content.replace(section.original, section.essentials);
    }
  }

  fs.writeFileSync(filePath, content);
  console.log(`Updated ${mod.file}`);
}

console.log('Done with batch 1');

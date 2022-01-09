import { Anchor, Box, Diagram, Heading, Paragraph, Stack } from "grommet";
import { Console } from "grommet-icons";
import "./HowItWorks.css";

interface HowItWorksProps {
  text: string;
}

const MarkovChainDiagram = (props: HowItWorksProps) => {
  const words = props.text.split(" ");
  const connections = [];

  let prev = null;
  const states: { [name: string]: string } = {};

  for (const word of words) {
    states[word] = "";

    if (prev !== null) {
      connections.push({
        fromTarget: prev,
        toTarget: word,
        thickness: "xsmall",
        type: "rectilinear" as any,
      });
    }

    prev = word;
  }

  return (
    <Box pad="large">
      <Stack>
        <Diagram connections={connections} />
        <Box>
          <Box
            wrap
            direction="row"
            align="center"
            className="chain-diagram"
            gap="large"
          >
            {Object.keys(states).map((word) => (
              <Box
                round
                key={word}
                id={word}
                pad={{ horizontal: "large", vertical: "small" }}
                background="brand"
              >
                {word}
              </Box>
            ))}
          </Box>
        </Box>
      </Stack>
    </Box>
  );
};

const Step = (props: any) => {
  return (
    <Box margin={{ top: "large" }} pad={{ horizontal: "medium" }}>
      {props.children}
    </Box>
  );
};

const Steps = () => {
  const exampleText = "This is a sample and this is another";

  return (
    <>
      <Step>
        <Heading fill size="small">
          1. Prepare the text
        </Heading>
        <Paragraph fill>
          Collect some text samples that the library can use to derive rules
          from. Let us take a simple sentence for now:
        </Paragraph>
        <Paragraph fill textAlign="center" className="source-text">
          {exampleText}
        </Paragraph>
      </Step>

      <Step>
        <Heading fill size="small">
          2. Build a Markov chain
        </Heading>
        <Paragraph fill>
          A{" "}
          <Anchor
            weight="bold"
            href="https://en.wikipedia.org/wiki/Markov_chain"
          >
            Markov chain
          </Anchor>{" "}
          is a probabilistic model that puts individual states - state being
          synonymous with a single word - into relation. States are linked by
          the likelihood with which a transition between them happens. Note that
          these transitions are directed so <code>A -&gt; B</code> does not
          imply <code>B -&gt; A</code>.
        </Paragraph>
        <MarkovChainDiagram text={exampleText} />
      </Step>

      <Step>
        <Heading fill size="small">
          3. Do a random walk
        </Heading>
        <Paragraph fill>
          We now pick a random start word and role a dice on each iteration.
          When transitioning to the next node, we output the name of our
          previous state. The so produced text will most likely be somewhat
          comprehensible because we have created our model on the basis of real
          examples:
        </Paragraph>
        <Paragraph fill textAlign="center" className="source-text">
          a sample and this is a sample and this is another
        </Paragraph>
        <Paragraph fill>
          Now imagine feeding this algortihm a bunch of Wikipedia pages and you
          will understand the fun behind ReMarkov.
        </Paragraph>
      </Step>
    </>
  );
};

export default function HowItWorks() {
  return (
    <Box direction="column" pad={{ vertical: "large" }}>
      <Box background="brand" margin={{ vertical: "large" }}>
        <Heading id="how-it-works" fill textAlign="center">
          How It Works
        </Heading>
      </Box>

      <Box fill="horizontal" align="center">
        <Box width="large">
          <Steps />
        </Box>
      </Box>
    </Box>
  );
}

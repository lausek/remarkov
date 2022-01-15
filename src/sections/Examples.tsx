import {
  Anchor,
  Box,
  Heading,
  RangeInput,
  Tabs,
  Tab,
  Text,
  ResponsiveContext,
} from "grommet";
import { useContext, useEffect, useState } from "react";
import "./Examples.css";
import examples from "./Examples.json";

const ExampleShowcase = () => {
  const [order, setOrder] = useState("1");
  const [output, setOutput] = useState("This is the output text.");

  const [selected, setSelected] = useState("Car Reviews");
  const [selectedSource, setSelectedSource] = useState("");

  const size = useContext(ResponsiveContext);

  useEffect(() => {
    const choice = (arr: Array<string>) => {
      const idx = Math.floor(Math.random() * arr.length);
      return arr[idx];
    };

    const exampleTextLoose = examples as any;
    const selectedExample = exampleTextLoose[selected];
    const texts = selectedExample.samples[order];
    const text = choice(texts);
    setOutput(text);
    setSelectedSource(selectedExample.source);
  }, [selected, order]);

  const onActive = (idx: any) => {
    const exampleName = Object.keys(examples)[idx];
    setSelected(exampleName);
  };

  return (
    <Box direction="column" gap="large">
      <Tabs onActive={onActive}>
        {Object.keys(examples).map((selectedExampleName) => {
          return <Tab key={selectedExampleName} title={selectedExampleName} />;
        })}
      </Tabs>

      <Box fill="horizontal" direction="column" gap="small">
        <Box
          round={size === "small" ? false : "medium"}
          fill
          background="window"
          pad="medium"
          className="showcase-output"
        >
          <Text>{output}</Text>
        </Box>

        <Box>
          <Text size="xsmall" textAlign="end">
            Based on dataset
            <Anchor
              href="https://github.com/lausek/remarkov/releases/tag/v0.2.3"
              target="_blank"
            >
              {selectedSource}
            </Anchor>
          </Text>
        </Box>
      </Box>

      <Box fill direction="row" pad={{ horizontal: "xlarge" }} gap="medium">
        <Text>Order</Text>
        <RangeInput
          min="1"
          max="4"
          step={1}
          value={order}
          onChange={(e) => setOrder(e.target.value)}
        />
      </Box>
    </Box>
  );
};

export default function Examples() {
  return (
    <Box fill="horizontal" pad={{ vertical: "large" }}>
      <Box background="brand">
        <Heading id="examples" fill textAlign="center">
          Examples
        </Heading>
      </Box>

      <Box fill="horizontal" align="center">
        <Box width="large" pad={{ vertical: "large" }}>
          <ExampleShowcase />
        </Box>
      </Box>
    </Box>
  );
}

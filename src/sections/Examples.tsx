import { Box, Heading, RangeInput, Text } from "grommet";
import { useEffect, useState } from "react";
import "./Examples.css";
import exampleText from "./ExampleText.json";

interface ExampleShowcaseSelectProps {
  name: string;
  value: string;
  onClick: (name: string) => void;
}

const ExampleShowcaseSelect = (props: ExampleShowcaseSelectProps) => {
  return (
    <Box
      className="showcase-select"
      pad="small"
      background={props.name === props.value ? "brand" : ""}
      onClick={() => props.onClick(props.name)}
    >
      {props.name}
    </Box>
  );
};

const ExampleShowcase = () => {
  const [order, setOrder] = useState("1");
  const [output, setOutput] = useState("This is the output text.");
  const [selected, setSelected] = useState("Car Reviews");

  useEffect(() => {
    const choice = (arr: Array<string>) => {
      const idx = Math.floor(Math.random() * arr.length);
      return arr[idx];
    };

    const exampleTextLoose = exampleText as any;
    const selectedExample = exampleTextLoose[selected];
    const texts = selectedExample["samples"][order];
    const text = choice(texts);
    setOutput(text);
  }, [selected, order]);

  return (
    <Box round background="light-2" pad="medium" gap="medium">
      <Box direction="row" gap="medium">
        <Box width="small" direction="column" gap="small" justify="between">
          <ExampleShowcaseSelect
            name="Car Reviews"
            value={selected}
            onClick={setSelected}
          />
          <ExampleShowcaseSelect
            name="Hotel Reviews"
            value={selected}
            onClick={setSelected}
          />
          <ExampleShowcaseSelect
            name="Horoscopes"
            value={selected}
            onClick={setSelected}
          />
          <ExampleShowcaseSelect
            name="Npc"
            value={selected}
            onClick={setSelected}
          />
          <ExampleShowcaseSelect
            name="Wiki Blockchain"
            value={selected}
            onClick={setSelected}
          />
        </Box>

        <Box fill="horizontal" direction="column" gap="medium">
          <Box
            fill
            background="light-4"
            pad="medium"
            className="showcase-output"
          >
            <Text>{output}</Text>
          </Box>
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

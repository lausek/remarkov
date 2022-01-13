import {
  Anchor,
  Box,
  Button,
  Footer,
  Grommet,
  Header,
  Heading,
  Main,
  Nav,
  Text,
} from "grommet";
import { grommet } from "grommet/themes";
import { CatalogOption, Console, Github, Moon, Sun } from "grommet-icons";
import { deepMerge } from "grommet/utils";

import Examples from "./sections/Examples";
import HowItWorks from "./sections/HowItWorks";
import { useState } from "react";


const config = {
  links: {
    github: "https://github.com/lausek/remarkov",
    docs: "https://lausek.eu/remarkov/docs/remarkov.html",
  },
};

const theme = deepMerge(grommet, {
  global: {
    colors: {
      brand: "#f91f1f",
      background: {
        dark: "#222",
      },
      focus: "brand",
      "graph-0": {
        light: "dark-1",
        dark: "light-4",
      },
    },
    font: {
      family: "Helvetica, Arial",
    },
  },
  anchor: {
    color: "brand",
  },
});

const PageFooter = () => {
  return (
    <Footer pad="large" justify="center">
      <Text size="small">
        2021
        <Anchor label="ReMarkov" href={config.links.github} />
        | Made by <Anchor label="lausek" href="https://lausek.eu" /> with <Anchor label="Grommet" href="https://v2.grommet.io/" />.
      </Text>
    </Footer>
  );
};

const Introduction = () => {
  return (
    <Box direction="column" margin={{ vertical: "large" }}>
      <Box pad="large">
        <Heading textAlign="center" size="large" margin={{ vertical: "small" }}>
          ReMarkov
        </Heading>
        <Text textAlign="center">
          A Python library for generating new text from existing samples.
        </Text>
      </Box>

      <Box pad={{ vertical: "large", horizontal: "xlarge" }} align="center">
        <Box
          round
          direction="row"
          gap="small"
          background="light-2"
          pad="medium"
          width="large"
        >
          <Console />
          <Text>pip3 install remarkov</Text>
        </Box>
      </Box>
    </Box>
  );
};

const JumpRightIn = () => {
  return (
    <Box direction="column" pad={{ vertical: "large" }}>
      <Box background="brand" margin={{ vertical: "large" }}>
        <Heading id="how-it-works" fill textAlign="center" size="small">
          Jump Right In
        </Heading>
      </Box>

      <Box fill="horizontal" align="center">
        <Box direction="row" gap="large">
          <Anchor
            size="large"
            label="Docs"
            href={config.links.docs}
            icon={<CatalogOption />}
          />
          <Anchor
            size="large"
            label="GitHub"
            href={config.links.github}
            icon={<Github />}
          />
        </Box>
      </Box>
    </Box>
  );
};

type ThemeMode = "light" | "dark";

const useLocalStorage = (
  name: string
): [ThemeMode, (themeMode: ThemeMode) => void] => {
  let currentTheme: ThemeMode = "light";
  try {
    currentTheme = localStorage.getItem(name) as ThemeMode;
  } catch {}

  const [themeMode, setThemeModeLive] = useState(currentTheme);
  const setThemeMode = (themeMode: ThemeMode) => {
    try {
      localStorage.setItem(name, themeMode);
    } catch {}

    setThemeModeLive(themeMode);
  };

  return [themeMode, setThemeMode];
};

function App() {
  const [themeMode, setThemeMode] = useLocalStorage("theme");
  const toggleTheme = () => {
    const nextTheme = themeMode === "light" ? "dark" : "light";
    setThemeMode(nextTheme);
  };

  return (
    <Grommet theme={theme} themeMode={themeMode}>
      <Header pad="medium">
        <Box fill="horizontal" />

        <Button onClick={toggleTheme}>
          {themeMode === "light" ? <Sun /> : <Moon />}
        </Button>

        <Nav direction="row">
          <Anchor
            label="Docs"
            href={config.links.docs}
            icon={<CatalogOption />}
          />
          <Anchor label="GitHub" href={config.links.github} icon={<Github />} />
        </Nav>
      </Header>

      <Main>
        <Introduction />
        <Examples />
        <HowItWorks />
        <JumpRightIn />
      </Main>
      <PageFooter />
    </Grommet>
  );
}

export default App;

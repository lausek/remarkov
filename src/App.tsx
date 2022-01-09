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
import { CatalogOption, Github, Moon, Sun } from "grommet-icons";
import { deepMerge } from "grommet/utils";

import Examples from "./sections/Examples";
import HowItWorks from "./sections/HowItWorks";
import React, { useState } from "react";

const config = {
  links: {
    github: "https://github.com/lausek/remarkov",
    docs: "https://github.com/lausek/remarkov",
  },
};

const theme = deepMerge(grommet, {
  global: {
    colors: {
      brand: {
        light: "#f91f1f",
        dark: "#f91f1f",
      },
      background: {
        dark: "dark-1",
      },
      focus: "brand",
    },
    font: {
      family: "Helvetica, Arial",
    },
  },
});

const PageFooter = () => {
  return (
    <Footer pad="large" justify="center">
      <Text size="small">
        2021
        <Anchor label="ReMarkov" href={config.links.github} />
        | Made with
        <Anchor label="Grommet" href="https://v2.grommet.io/" />
      </Text>
    </Footer>
  );
};

const Introduction = () => {
  return (
    <Box fill="horizontal" pad={{ vertical: "large" }}>
      <Heading fill textAlign="center" size="large">
        ReMarkov
      </Heading>
      <Text textAlign="center">
        Generate text from text using Markov chains.
      </Text>
      <Box pad="medium" />
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
    <Grommet full theme={theme} themeMode={themeMode}>
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
        <HowItWorks />
        <Examples />
      </Main>
      <PageFooter />
    </Grommet>
  );
}

export default App;

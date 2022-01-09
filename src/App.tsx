import {
  Anchor,
  Box,
  Footer,
  Grommet,
  Header,
  Heading,
  Main,
  Nav,
  Text,
} from "grommet";
import { grommet } from "grommet/themes";
import { CatalogOption, Github } from "grommet-icons";
import { deepMerge } from "grommet/utils";

const config = {
  links: {
    github: "https://github.com/lausek/remarkov",
    docs: "https://github.com/lausek/remarkov",
  },
};

const theme = deepMerge(grommet, {
  global: {
    colors: {
      brand: "#f91f1f",
      focus: "brand",
    },
    font: {
      family: "Helvetica, Arial",
    },
  },
});

const PageHeader = () => {
  return (
    <Header pad={{ vertical: "small", horizontal: "large" }}>
      <Box fill="horizontal" />
      <Nav direction="row">
        <Anchor
          label="Docs"
          href={config.links.docs}
          icon={<CatalogOption />}
        />
        <Anchor label="GitHub" href={config.links.github} icon={<Github />} />
      </Nav>
    </Header>
  );
};

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
    <Box fill="horizontal" pad="medium">
      <Heading textAlign="center">ReMarkov</Heading>
      <Text textAlign="center">
        Generate text from text using Markov chains.
      </Text>
      <Box pad="medium" />
    </Box>
  );
};

const HowItWorks = () => {
  return <></>;
};

function App() {
  return (
    <Grommet theme={theme}>
      <PageHeader />
      <Main>
        <Introduction />
        <HowItWorks />
      </Main>
      <PageFooter />
    </Grommet>
  );
}

export default App;

import { Box, Heading } from "grommet";

export default function Examples() {
  return (
    <Box fill="horizontal" pad={{ vertical: "large" }}>
      <Box background="brand">
        <Heading id="examples" fill textAlign="center">
          Examples
        </Heading>
      </Box>
    </Box>
  );
}

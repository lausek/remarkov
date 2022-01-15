# ReMarkov Website

## Rebuild site

```bash
npm run build
rm -rf docs/
mv build/ docs/
```

## Update Documentation

```bash
pdoc -t pdoc/template -o public/docs <path_to_remarkov_module>
```

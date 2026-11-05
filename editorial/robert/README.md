# Robert — *Obra sobre papel*

Coleção de três livros de arte feita a partir de 16 obras sobre papel.

| Volume | Título | Assunto | Obras | Páginas |
|---|---|---|---|---|
| I | **Linha** | Desenhos a tinta (preto e sépia) | 07, 09, 11, 14, 06, 10 | 24 |
| II | **Escrita** | Caligrafias inventadas (escrita assêmica) | 01, 08, 03, 15 | 20 |
| III | **Cor** | Gesto e figura | 02, 04, 12, 05, 13, 16 | 24 |

## Especificações
- Formato: 30 × 24 cm, paisagem. Sangria de 3 mm já incluída nos PDFs.
- Capa dura. Arte da capa em uma única folha (verso, lombada e frente), lombada de 10 mm. **A lombada, a dobra e a margem de virada da capa dura precisam ser confirmadas pelo gabarito da gráfica.**
- Tipografia: Instrument Serif (títulos), Newsreader (texto), Inter Tight (rótulos), IBM Plex Mono (dados de catálogo).
- Cor por volume: preto-tinta, vermelhão e ultramar.

## Arquivos
- `pdf/vol-*.pdf`: miolo de cada volume (prova digital).
- `pdf/capa-*.pdf`: capas.
- `preview/`: mockup da coleção, espelhos de página e capas.
- `plates/`: obras digitalizadas (perspectiva corrigida, luz uniformizada, papel neutralizado).
- `works.json`: **todos os textos editáveis** (títulos, técnicas, ensaios, epígrafes e cortes).

## Para reconstruir
```bash
python3 scripts/process.py   # src/ -> plates/
python3 scripts/details.py   # escolhe os recortes de detalhe
python3 scripts/build.py     # gera o HTML
node scripts/render.js       # gera os PDFs
```

## Antes de imprimir
As imagens de origem são fotos de celular de cerca de 2000 px, o que dá uns 190 dpi nas pranchas inteiras e menos nos detalhes ampliados. Para a gráfica, as obras devem ser escaneadas ou refotografadas a 600 dpi. Basta substituir os arquivos em `src/` e rodar os scripts de novo; a diagramação se ajusta sozinha.

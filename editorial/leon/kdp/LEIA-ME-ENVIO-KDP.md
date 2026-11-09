# Leon's Thinking Book: envio para a Amazon KDP

Há 12 arquivos: 2 volumes × 3 línguas, cada um com miolo e capa.

| Volume | Língua | Miolo | Capa |
|---|---|---|---|
| 1 (4–6 anos) | EN / FR / NL | `leons-thinking-book-vol1-XX-interior.pdf` | `leons-thinking-book-vol1-XX-cover.pdf` |
| 2 (6–8 anos) | EN / FR / NL | `leons-thinking-book-vol2-XX-interior.pdf` | `leons-thinking-book-vol2-XX-cover.pdf` |

## Configurações no KDP (Paperback, igual para os 6 livros)
- **Ink and paper type:** Standard color, white paper.
- **Trim size:** 8.5 × 11 in (21,59 × 27,94 cm).
- **Bleed settings:** *Bleed* (as páginas já têm 0,125 in de sangria).
- **Paperback cover finish:** Matte.
- **Páginas:** 80. A lombada fica com 0,1878 in, só cor e sem texto, como decidido no projeto (com menos de 5 mm de largura, um texto na lombada não ficaria legível).
- **ISBN:** use o ISBN gratuito do KDP ou um próprio. O código de barras é colocado pelo KDP na área branca do canto inferior direito da contracapa (2 × 1,2 in).

## Verificação automática (`VERIFICACAO-KDP.txt`)
- **Tamanho:** miolo com 8,625 × 11,25 in; capa com 17,4378 × 11,25 in.
- **Páginas:** 80 em cada miolo.
- **Fontes:** todas incorporadas.
- **Imagens:** todas a 300 dpi ou mais no tamanho impresso. As 4 imagens "300 dpi" nas capas são sombras geradas pelo renderizador, exatamente a 300 dpi.

## O que mudou em relação aos PDFs anteriores
- **Volume 1:** 19 páginas agora usam obras reais de Robert de Farias: p.10, 14, 17, 18, 19, 20, 21, 22, 28, 30, 31, 33, 36, 37, 42, 43, 45, 60 e 64.
- **Volume 2:** 20 páginas com obras reais: p.8, 11, 12, 15, 19, 20, 21, 22, 23, 24, 27, 28, 29, 30, 32, 34, 53, 55, 62 e 66. Rostos aparecem só aqui.
- **Gabaritos:** foram refeitos com as novas respostas. No V1 há uma miniatura com círculo vermelho para a resposta de posição (p.64).
- **EN:** "Brain Challenge" foi trocado por "Big Challenge" e "Final Brain Challenge" por "Final Big Challenge".
- **p.4 do V1 (3 línguas):** a frase de venda agora é honesta ("Many of the games are made with real artworks…"), em vez de "Every page…".
- **Capas novas:** o Leon foi aproveitado em vetor e as obras reais estão integradas.
- **IMG_0403:** não é usada em lugar nenhum.

## Antes de clicar em "Publish" (recomendado)
1. **Revisão nativa** dos textos novos em FR e NL (títulos, instruções e respostas das páginas com obras, além das capas).
2. **Previewer do KDP:** abrir cada livro e conferir.
3. **Cópia de prova (proof copy):** pedir uma impressa de cada volume pelo menos, para ver as cores e a nitidez.
4. **Resolução das obras:** as fotos foram ampliadas por um processo clássico (Lanczos e nitidez) para chegar a 300 dpi. Se tiver os **arquivos originais do telemóvel** (normalmente 4032 × 3024 px; os que chegaram pelo chat tinham 2016 × 1512), envie-os pelo Google Drive ou WeTransfer. Basta substituí-los e rodar os scripts outra vez para ganhar nitidez real.

## Como regenerar
```bash
cd editorial/robert && python3 scripts/process.py && python3 scripts/hd.py
cd ../leon && PLATES=../robert/plates_hd python3 scripts/art_prep.py
python3 scripts/kdp/compose.py V1 && python3 scripts/kdp/compose.py V2 && python3 scripts/kdp/covers.py
python3 scripts/kdp/check_pdf.py build/kdp/leons-*.pdf
```

> ⚠️ Esta pasta é a versão anterior (80 páginas). A versão em vigor do V1 EN está em `../kdp-v1-revisado/`.

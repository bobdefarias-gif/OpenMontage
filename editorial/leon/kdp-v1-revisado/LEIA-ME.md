# Leon's Thinking Book: Volume 1, edição revista (96 páginas), EN · FR · NL

Esta edição substitui a pasta `kdp/` anterior, que tinha 80 páginas. Aplica a revisão completa de `docs/revisao-v1/`.

## Configurações no KDP (Paperback)
- **Ink and paper:** Standard color, white paper.
- **Trim size:** 8.5 × 11 in.
- **Bleed:** Bleed. As páginas já incluem 0,125 in de sangria.
- **Cover finish:** Matte.
- **Páginas:** 96. Lombada de 0,2253 in, só cor e sem texto.
- **Capa completa:** 17,4753 × 11,25 in. A área do código de barras está livre no canto inferior direito da contracapa.

## Verificação técnica (`VERIFICACAO-KDP.txt`)
- **Tamanho e páginas:** tamanhos exatos; 96 páginas no miolo.
- **Fontes:** todas incorporadas (Andika, Baloo 2, Lexend).
- **Imagens:** todas a 300 dpi ou mais.
- **Margem segura:** todo o texto fica a pelo menos 0,375 in do corte.
- **Termos proibidos:** nenhuma ocorrência de "brain" no livro.

## O que mudou
- **Arte e texto:** a arte original das atividades foi mantida em vetor e todo o texto foi recomposto em Andika.
- **Navegação:** cada página tem etiqueta da ilha, estrelas de nível e rodapé com o nome da ilha e da habilidade.
- **Páginas novas:** "Meet Leon & Luz", guia "Hello, grown-ups!" em 2 páginas, "How to use" com 3 níveis e o quadro de estrelas por ilha.
- **10 aberturas de ilha:** cada uma tem uma pintura de Robert e uma pergunta "Art Detective".
- **Atividades redesenhadas:**
  - p.27 Look, cover, draw: 3 níveis e caixas maiores.
  - p.39: instrução corrigida.
  - p.40: com exemplos.
  - p.45: 4.ª adivinha.
  - p.54: Luz no fim do caminho e "Super path" até 15.
  - p.64: legenda "dish".
  - p.67: ordens de 1, 2 e 3 passos.
  - p.77: carinhas reordenadas.
  - p.78: várias respostas aceites.
  - p.81: inglês corrigido.
- **Emoções e mini-missão:** "Everyday feelings" (p.79), "Same day, different feelings" (p.80) e a Picnic Mission em 2 páginas (p.87–88).
- **Caixas para pais:** Parent's Little Tip, Ask Leon, Talk About It e Try Another Way, na maioria das páginas.
- **Gabarito:** p.91–95, com as respostas de todas as páginas novas e revistas.
- **Capa:** passou para 96 páginas, com texto da contracapa honesto.

## Antes de publicar
1. **Revisão por falantes nativos** (EN, FR e NL-BE) de todo o texto novo.
2. **Previewer do KDP.**
3. **Cópia de prova impressa:** verificar a cor das pinturas e a legibilidade a preto e branco.
4. **Teste com crianças** (recomendado). Ver `docs/revisao-v1/07-controle-de-qualidade.md`. O livro ainda não foi testado com crianças.

## Limitações conhecidas
- **Pinturas:** vêm de fotos de celular ampliadas para 300 dpi. Os originais em alta resolução melhoram a nitidez; basta regenerar.
- **Caixas opcionais:** 1 caixa não coube na p.16, porque a atividade ocupa a página.
- **FR e NL:** prontos. Os textos das atividades que não mudaram vêm dos PDFs FR/NL originais. Os textos novos (guia para pais, aberturas, caixas, páginas novas e respostas novas) foram traduzidos por mim e **precisam da revisão de um falante nativo**.

## Regenerar (trocar XX por EN, FR ou NL)
```bash
V1R_LANG=XX python3 scripts/v1r/build.py
PAGES=96 COVER_OUT=build/v1r/XX/leons-thinking-book-vol1-XX-cover-revised.pdf python3 -c "import sys;sys.path.insert(0,'scripts/kdp');import covers;covers.build('V1','XX')"
PAGES=96 python3 scripts/kdp/check_pdf.py build/v1r/XX/*revised.pdf
```

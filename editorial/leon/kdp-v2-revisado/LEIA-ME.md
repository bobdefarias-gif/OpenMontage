# Leon's Thinking Book: Volume 2, edição revista (96 páginas), EN · FR · NL

Substitui os PDFs de 80 páginas do V2 em `kdp/`.

## Configurações no KDP (Paperback)
- **Ink and paper:** Standard color, white paper.
- **Trim size:** 8.5 × 11 in.
- **Bleed:** Bleed (0,125 in já incluído).
- **Cover finish:** Matte.
- **Páginas e lombada:** 96 páginas; lombada de 0,2253 in, só cor e sem texto.
- **Capa:** 17,4753 × 11,25 in; área do código de barras livre no canto inferior direito da contracapa.

## Verificação (`VERIFICACAO-KDP.txt`)
- **Tamanho e páginas:** tamanhos exatos; 96 páginas.
- **Fontes:** todas incorporadas (Andika, Baloo 2, Lexend); nenhuma fonte de sistema.
- **Imagens:** todas a 300 dpi ou mais.
- **Margem e termos:** todo o texto dentro da margem segura; nenhuma ocorrência de "brain".

## Auditoria do original
- **Atividades e gabarito:** conferi as 68 atividades contra as imagens; as 60 respostas do gabarito estão corretas.
- **Problemas corrigidos:**
  - "Final Brain Challenge" passou a "Final Big Challenge";
  - os nomes das missões ficaram consistentes (rodapé "Planning & Flexibility" / "Emotional Skills" → "Planning" / "Feelings");
  - a frase de venda foi corrigida;
  - as referências "page 75" foram atualizadas para a nova paginação.

## O que mudou
- **Missões e aberturas:** as 12 missões originais continuam; cada uma abre com uma pintura de Robert e uma pergunta "Art Detective".
- **Atividades originais:** as 68 foram mantidas (arte vetorial original) e o texto foi recomposto nas fontes novas, com etiqueta da missão, estrelas e rodapé.
- **Atividade nova (p.24):** "Remember the order", memória auditiva com detalhes das pinturas. Mantém as páginas "olhar" em página ímpar.
- **Páginas de abertura:** guia para pais em 2 páginas, "Meet Leon & Luz" e "How to use" com os 3 níveis.
- **Caixas e gabarito:** caixas de dica na maioria das páginas; gabarito nas p.92–95.
- **Atualizações:** "Mission tracker" e mapa com a nova paginação; certificado com texto de esforço ("for thinking, planning and never giving up!").

## Antes de publicar
1. **Revisão nativa** (EN, FR, NL-BE) dos textos novos. As atividades que não mudaram usam o texto dos PDFs FR/NL originais.
2. **Previewer do KDP** e **cópia de prova impressa**.
3. **Teste com crianças** (recomendado; ainda não feito).

## Limitações
- **Caixas opcionais:** algumas não cabem em páginas cheias e foram omitidas de propósito.
- **Pinturas:** vêm de fotos ampliadas para 300 dpi. Os originais em alta resolução melhoram a nitidez.

## Regenerar (XX = EN, FR ou NL)
```bash
V2R_LANG=XX python3 scripts/v2r/build.py
PAGES=96 COVER_OUT=build/v2r/XX/leons-thinking-book-vol2-XX-cover-revised.pdf python3 -c "import sys;sys.path.insert(0,'scripts/kdp');import covers;covers.build('V2','XX')"
PAGES=96 python3 scripts/kdp/check_pdf.py build/v2r/XX/*revised.pdf
```

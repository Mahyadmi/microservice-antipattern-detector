# Dissertation presentation & viva materials

Web pages used to present and defend the MSc dissertation
**"Cloud-Native Detection of Microservice Anti-Patterns using Static Analysis Tools and Serverless Architectures"**
(Staffordshire University, 2025).

**View online:** https://mahyadmi.github.io/microservice-antipattern-detector/presentation/

| Page | What it shows |
|------|---------------|
| [`index.html`](index.html) | Start page linking all materials |
| [`viva-presentation.html`](viva-presentation.html) | 7-slide viva deck (use ← → keys or swipe) |
| [`viva-summary.html`](viva-summary.html) | One-page visual summary: problem → solution → results |
| [`demo-architecture.html`](demo-architecture.html) | Architecture walkthrough: containers, detection flow, results, code structure, frontend &amp; backend with dashboard screenshots |
| [`semantic-similarity.html`](semantic-similarity.html) | How duplicate findings are matched with TF-IDF + cosine similarity (worked example with runnable code) |

## Key results (from the dissertation)

- **Precision 100%**, **recall 66.7%**, **F1 80%**. This was a preliminary validation on 2 files with 6 known anti-patterns.
- Tested on **gs-spring-boot**, **spring-petclinic-microservices**, **sock-shop** and **eShopOnContainers**, finding 2–6 patterns per project in ~5–35 seconds.
- Projected cost **~£0.04 per analysis** on AWS serverless pricing.
- Serverless AWS design simulated locally with **Docker Compose**.

`img/` holds the dashboard screenshots from the four test projects. The pages are plain HTML. Open any of them in a browser; nothing needs installing.

# Data snapshot — Values Under Fire

Generated: 2026-05-22T12:55:22

## Repositories

- values-under-fire: `/Users/danieltenner/dev/research/values-under-fire` @ `d40d99b96e4d906e0614bb1718b4bf69ea9e7cd3`
- model-personality-analysis-corpus: `/Users/danieltenner/dev/research/model-personality-analysis-corpus` @ `9fb17c011576b4de873cf61856cb693da0ef2833`
- model-personality-corpus-v2: `/Users/danieltenner/dev/research/model-personality-corpus-v2` @ `c5af0c28cde2335c7508ee4253a3414b2763f841`
- corpus-v2 latest tag: `v1.2.1`

## Input file hashes

| file | rows | sha256 |
|---|---:|---|
| `manifest_valid.jsonl` | 13906 | `f3713baf8bf5d2800e173039b5a4104eedc3865669049bd413e87863205ec77d` |
| `manifest_invalid_traces.jsonl` | 14 | `de284c163d5a818eadaa70a0f3bc812fe6b10bbd49511c4fd894c09f94be47b3` |
| `layer_a_consensus.jsonl` | 13906 | `50023adaf59bef9fe8c215c02cde23d7e7c464f6b66b58314ddde3e09f55d7e0` |
| `posture_consensus.jsonl` | 13906 | `7c9cbbbf74adb3f70046223f08ed7196d2ebe2768b3dc6dc79cf1c8ce84ef76e` |
| `layer_a_coder_glm-4-7.jsonl` | 13906 | `0ece9cc70f15155433993c625540cb3734d0e54480001058da1984a0bff7086c` |
| `layer_a_coder_kimi-k2-6.jsonl` | 13906 | `671d4b9115b19befd7b5b9926bcdf099df10a31897df8433df12c60e6fae8637` |
| `layer_a_coder_qwen3-6-35b-a3b.jsonl` | 13906 | `a9183877bbfa995af3c34bbd4ca333a06f030b8c083b1516b63a23ea182be2cf` |
| `posture_coder_glm-4-7.jsonl` | 13906 | `629b514cc83c2a3d976e395744883c22e9b66674b82c98bdf5edcd4934b24ab3` |
| `posture_coder_kimi-k2-6.jsonl` | 13906 | `4711ecd81af46421a32e02e5a8453ce16053c4a950d8282f588013b7d5c0cd35` |
| `posture_coder_qwen3-6-35b-a3b.jsonl` | 13906 | `45ad3519fdf73ac6be014f85daf51a443d052f0503b223394bbdccb177f45d8f` |

## Join/exclusion counts

- valid manifest rows: 13,906
- invalid trace rows: 14
- analysed rows after required joins: 13,906
- exclusions beyond invalid traces: 0

## Counts by condition

| condition | rows |
|---|---:|
| CTRL1 | 1,160 |
| CTRL2 | 1,160 |
| CTRL3 | 1,158 |
| G1 | 3,473 |
| G2 | 3,478 |
| G3 | 3,477 |

## Model alias normalization

The analysis aggregates known alternate labels for the same underlying model at model level, while preserving source cells in the tidy table.

| source model | canonical model |
|---|---|
| `grok-4-20` | `grok-4-2` |

## Counts by lab

| lab | models | rows |
|---|---:|---:|
| Anthropic | 9 | 1,440 |
| DeepSeek | 3 | 2,148 |
| Google | 11 | 1,320 |
| MiniMax | 2 | 598 |
| Moonshot AI | 5 | 1,200 |
| OpenAI | 13 | 1,800 |
| Qwen | 2 | 240 |
| Z.ai | 6 | 4,200 |
| xAI | 6 | 960 |

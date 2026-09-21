Lab 1: The price of one request
Student: Akim Lunara
Course: AI CSS4007-ENG-5
1.	Prediction from Part1 and measured values
Tokenizers are typically trained primarily on English text, so they handle Russian better than Kazakh. Consequently, Russian text results in fewer tokens than the raw byte count would suggest, whereas Kazakh—which includes rare characters like ә, ғ, қ, ң, ө, ұ, ү, һ, and і—likely yields an equal or greater number of tokens. English text averages about one token per four characters, or roughly 1.3 tokens per word. For Russian and Kazakh, one generally expects 1.5 to 3 times as many tokens as for English, depending on the specific tokenizer.
COMPLAINT
| Metric | English (EN) | Russian (RU) | Kazakh (KK) |
|---|---:|---:|---:|
| Characters | 300 | 315 | 344 |
| Bytes | 300 | 576 | 640 |
| Words | 54 | 45 | 42 |
| Bytes / EN | 1.00× | 1.92× | 2.13× |
| Bytes / character | 1.00 | 1.83 | 1.86 |

counting tokens on gemini-3-flash-preview (free, no model run)
  sentence       en=13  ru=18  kk=31
  complaint      en=60  ru=79  kk=149
  system_prompt  en=41  ru=52  kk=88
  request        en=101  ru=131  kk=237  

RU / EN - 79 / 60 = 1.32x
KK / EN - 149 / 60 = 2.48x

2.	Table of annual cost

AT 2,000 REQUESTS/DAY -- US dollars per year
------------------------------------------------------------------------
                        EN          RU          KK
flash-lite-3.1       1,344         971       1,333
flash-3              2,689       1,942       2,666
pro-3.1             10,756       7,769      10,665

AT 5,000 REQUESTS/DAY -- US dollars per year
------------------------------------------------------------------------
                        EN          RU          KK
flash-lite-3.1       3,361       2,428       3,333
flash-3              6,722       4,855       6,666
pro-3.1             26,890      19,422      26,663
5,000 requests per day represents a high-volume support queue, so the annual cost shows how token usage and model choice can affect the budget at production scale.
3.	Which model for Kazakh languages
Based on the quality of the responses and the pricing, I would choose the Flash Light 3.1 model; the cost is reasonable, and I liked the way the query was handled—there was no guesswork involved. Instead, the representative asked the client to try a few potentially helpful steps and advised them to contact the bank or provide the missing information needed to resolve the issue if those steps didn't work.
4.	Suggestions
Limit the response length and the "thinking" budget, because output tokens account for almost the entire cost; system prompt caching reduces only the small input 

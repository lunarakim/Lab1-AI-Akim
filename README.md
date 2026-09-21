Lab 1: The Price of One Request

Student: Akim Lunara
Course: AI CSS4007-ENG-5

1. Prediction from Part 1 and Measured Values

Tokenizers are typically trained primarily on English text, so they
generally handle Russian better than Kazakh. Consequently, Russian text
may result in fewer tokens than the raw byte count would suggest,
whereas Kazakh---which includes less common characters such as ә, ғ,
қ, ң, ө, ұ, ү, һ, і---is expected to produce an equal or greater
number of tokens.

English text averages about one token per four characters, or roughly
1.3 tokens per word. For Russian and Kazakh, one may generally expect
1.5--3 times as many tokens as for English, depending on the tokenizer.

Text: COMPLAINT

Metric                English (EN)   Russian (RU)   Kazakh (KK)

Characters                     300            315           344
Bytes                          300            576           640
Words                           54             45            42
Bytes / EN                   1.00×          1.92×         2.13×
Bytes / character             1.00           1.83          1.86

Measured Token Counts

Token counting was performed using gemini-3-flash-preview (free,
without running the model).

Text                  EN       RU        KK

Sentence              13       18        31
Complaint     60   79   149
System prompt         41       52        88
Request              101      131       237

Comparison with English

Russian / English:

79 / 60 = 1.32×

Kazakh / English:

149 / 60 = 2.48×

The measured results show that the Russian complaint required about
1.32 times as many tokens as the English version, while the Kazakh
complaint required about 2.48 times as many tokens.

This demonstrates that byte size and token count are related but not
equivalent. In particular, Kazakh text produced substantially more
tokens in this experiment.

2. Table of Annual Cost

The following calculations assume the stated request volume and compare
the annual cost in US dollars.

2,000 Requests per Day

Model                    EN        RU         KK

flash-lite-3.1      $1,344     $971    $1,333
flash-3             $2,689   $1,942    $2,666
pro-3.1            $10,756   $7,769   $10,665

5,000 Requests per Day

Model                    EN         RU         KK

flash-lite-3.1      $3,361    $2,428    $3,333
flash-3             $6,722    $4,855    $6,666
pro-3.1            $26,890   $19,422   $26,663

At 5,000 requests per day, the system represents a high-volume
support queue. The annual cost illustrates how token usage and model
selection can affect the budget when the system is used at production
scale.

3. Which Model for the Kazakh Language?

Based on the response quality and pricing considered in this experiment,
I would choose the Flash Lite 3.1 model.

The cost is relatively reasonable, and I liked the way the query was
handled. The response did not rely on guesswork. Instead, the
representative asked the client to try several potentially helpful steps
and advised them to contact the bank or provide the missing information
needed to resolve the issue if those steps did not work.

Therefore, for this particular support scenario, Flash Lite 3.1
provides a practical balance between response quality and cost.

4. Suggestions

I would recommend limiting the response length and the thinking
budget, because output tokens account for a significant part of the
total cost. System-prompt caching reduces only the input portion of the
cost, so controlling unnecessary output can have a larger effect on the
overall budget.

Possible cost-control measures include:

limiting unnecessary response length;

setting an appropriate thinking budget;

keeping system prompts concise;

using prompt caching where applicable;

selecting a less expensive model for high-volume routine requests.

Declaration of AI Use

I primarily used Claude AI to understand the workflow and the steps
required to obtain an API key.

Claude explained that the Anthropic API key is a paid service, so it
suggested using Gemini and working in Google Colab for
convenience, noting that the setup operates within the Google ecosystem.
It also proposed using the terminal as an alternative.

Since I successfully generated the required outputs and the code ran
properly, I completed the practical work in Google Colab.

Claude also helped adapt the code for Gemini AI. We modified the code in
the part2, part3, and price files, as well as the data in the
text file. Claude provided the pricing figures, which I verified
against the official Gemini API pricing documentation:

Official pricing: https://ai.google.dev/gemini-api/docs/pricing

During execution, I encountered 400, 503, and 429 errors. Claude
helped me understand the meaning of these errors and resolve the 400
error by using an API key from my personal Google account instead of a
corporate account.

Conclusion

This lab demonstrated how language, tokenization, model selection, and
request volume can affect the cost of using an AI model.

The experiment showed that the same complaint can require substantially
different numbers of tokens depending on the language. In this case, the
Kazakh version used significantly more tokens than the English version.
Therefore, language-specific tokenization should be considered when
estimating the cost of an AI-powered support system.

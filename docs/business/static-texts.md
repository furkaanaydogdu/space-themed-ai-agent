# Static Texts: Discover the Cosmos

## Purpose

This document lists the fixed texts the product shows and what the agent's own explanations must say. Every other message in the conversation is written by the agent for each question. The fixed texts exist for the situations where the product itself has to speak, and as backups for the situations where the agent cannot.

## 1. System messages

These are shown when the product itself, not the agent, has to speak. Each one appears in the conversation as a plain reply in place of the thinking indicator, except where the table says otherwise.

| Situation | When it happens | Text | What else happens |
| --- | --- | --- | --- |
| Timeout | An answer takes too long and the request is cut off | “That took longer than I could wait, so I stopped. Your question is back in the box. Try again, or ask something simpler.” | The question returns to the input box. |
| Failed request | The request fails for any other reason, such as a lost connection or a server error | “Something went wrong and I couldn’t get an answer. Your question is back in the box. Press Ask to try again.” | The question returns to the input box. |
| Sign-in expired | The visitor’s sign-in has run out | “Your sign-in has expired. The page will reload so you can sign in again.” | The page reloads, the visitor signs in again, and the conversation is restored. |
| Question too long | The visitor reaches 300 characters | A hint under the input: “Questions can be up to 300 characters.” | The field stops accepting characters at the limit. No error message. |
| Conversation can’t be saved | The browser blocks saving, or the saved conversation no longer fits | “This page can’t save the conversation in your browser, so it will be lost if you reload or close the tab.” | Shown once per tab. The conversation keeps working on screen. |
| Empty asteroid week | NASA’s data lists no near-Earth asteroids for the 7-day window | “NASA’s data lists no near-Earth asteroids passing Earth between 2 and 9 Nov.” (the dates are those of the window) | No overlay, no chip and no example questions. In a mixed question the sentence is added to the overview sentence. |

## 2. What the agent’s explanations must say

Refusals and other explanations are written by the agent for each question. They are short, about three sentences, and never answer the question or hint at its answer. When a question has an answerable part and a part the product cannot answer, the answerable part is answered and the explanation is added after the overview sentence. Each reason must cover the following points.

| Reason | The explanation must |
| --- | --- |
| The question relies on an earlier answer | Say that each question is answered on its own. Ask the visitor to name what they mean, such as a picture’s title. Point to the earlier answer in the conversation, which can be reopened. |
| The question is outside what the product can answer, including questions about one specific asteroid, comparisons between asteroids, and one point on the ISS path | Explain plainly what the product can answer: the picture archive, near-Earth asteroids for the next 7 days, and the ISS’s current position and path. The four example questions follow it. |
| Nothing in the picture archive matches | Say that nothing matched well, say what the archive covers (roughly the last two years), and suggest describing the picture another way. |
| A source is unavailable | Say which part could not be loaded and invite the visitor to try again later. Any part that did load is still shown. |
| The agent stops itself because the answer is taking too long | Say that it stopped because it was taking too long, and invite the visitor to try again or ask something simpler. The question returns to the input box. |

## 3. Backup messages for refusals

These are used when the agent cannot write its own message safely, for example when it fails or when its message states something the product’s data does not support. There is one for each reason.

| Reason | Text |
| --- | --- |
| The question relies on an earlier answer | “I answer each question on its own, so I can’t tell what you’re referring to. Please name it, for example a picture’s title. Your earlier answer is still in the conversation above: tap it to open it again.” |
| Outside what the product can answer | “I can’t answer that one. I only use three sources: NASA’s Astronomy Picture of the Day archive, near-Earth asteroids for the next 7 days, and the ISS’s current position and path. You could try one of these:” followed by the four example questions. On a phone: “I can’t answer that one. I only use NASA’s picture archive, near-Earth asteroids for the next 7 days, and the ISS’s position and path. You could try:” |
| Nothing in the picture archive matches | “I couldn’t find a good match for that in NASA’s picture archive, which covers roughly the last two years. Try describing it another way, for example by its name or what it shows.” |
| A source is unavailable | “I couldn’t reach {NASA’s picture archive / NASA’s asteroid data / the ISS position service} just now, so that part is missing. Please try again in a moment.” |
| The answer is taking too long | The same text as the timeout system message in section 1. |

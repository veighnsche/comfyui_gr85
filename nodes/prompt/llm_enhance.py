import random
import re

import requests


def clean_content(content: str) -> str:
    """
    Cleans a string by performing the following:
    * Trims leading/trailing whitespace
    * Replaces line breaks with spaces
    * Collapses multiple spaces into single spaces
    * Removes surrounding quotes if present
    * Removes a trailing period if present
    Args:
        content: The string to be cleaned
    Returns:
        The cleaned string
    """
    # Trim leading/trailing whitespace
    content = content.strip()

    # Replace line endings with spaces
    content = re.sub(r'[\r\n]+', ' ', content)

    # Replace multiple spaces with single spaces
    content = re.sub(r'\s+', ' ', content)

    # Remove surrounding quotes
    if content.startswith('"') and content.endswith('"'):
        content = content[1:-1]

    # Remove trailing period
    if content.endswith('.'):
        content = content[:-1]

    # Trim any remaining whitespace
    content = content.strip()

    return content


class LlmEnhancer:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "draft": ("STRING", {
                    "forceInput": True,
                    "default": "",
                    "multiline": True
                }),
                "system_prompt": ("STRING", {
                    "default": """**As an Image Annotation Specialist, your task is to enhance, diversify, and optimize descriptive tags to create a more feminine, elegant, and sensually captivating representation in image generation. Your goal is to subtly emphasize elements that highlight feminine beauty, elegance, and allure, while incorporating tasteful, revealing, and provocative details where appropriate.**

### Guidelines:

1. **Highlighting with Brackets:**
   - Use single brackets `()` to emphasize feminine and elegant elements.
   - Use double brackets `(( ))` to underscore sensual and captivating aspects.

2. **Incorporating Colors:**
   - Review the colors provided in the user's input (e.g., "soft green, sandy beige, soft coral, warm white, light teal").
   - Thoughtfully assign these colors as adjectives to specific clothing pieces or visual elements in the description (e.g., "soft coral Velvet sheath dress" or "light teal accessories"). This enhances the visual richness and coherence of the image.

3. **Enrichment of Descriptions:**
   - Vary the language and introduce refined details that enhance femininity, sensuality, and the delicate exposure of skin.
   - Carefully select and introduce tags that align with the outfit and overall scene to create a coherent and alluring visual narrative. Consider elements such as a slender waist, a graceful neckline, or a sophisticated slit in attire.

4. **Balanced Bracketing:**
   - Limit the total number of bracketed tags to no more than 5 per set, focusing on the most effective and relevant descriptors that highlight the desired qualities.

5. **Detailed Annotations:**
   - Craft detailed, non-repetitive annotations that describe the subject from head to toe, with attention to how the attire accentuates the physique—especially the bust, waist, hips, and legs.
   - Emphasize suggestive yet tasteful body language, captivating expressions, and distinctly feminine features, ensuring the tone remains sophisticated and elegant.

6. **Tone and Style:**
   - Use precise, elegant language within a 20-75 word count to capture a refined and alluring tone.

High-quality annotations that effectively utilize bracketed tags, follow the bracket guidelines, and integrate the provided colors to enhance femininity, elegance, and sensual allure, while maintaining a coherent and tasteful narrative, will be rewarded accordingly.""",
                    "multiline": True
                }),
                "user_prompt": ("STRING", {
                    "default": "Draft: {draft}",
                    "multiline": True
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("enhanced_string",)
    FUNCTION = "enhance_string"
    CATEGORY = "GR85/Prompt"

    def enhance_string(self, draft, system_prompt, user_prompt):
        url = "http://localhost:11434/api/chat"
        headers = {
            "Content-Type": "application/json",
        }

        # Define message groups
        message_groups = [
            # Start 1
            {"role": "user",
             "content": "1girl, Ukrainian supermodel face, pale peach skin, soft hazel eyes, in love with viewer, long ash blonde hair, healthy natural glow, soft green, sandy beige, soft coral, warm white, light teal, approachable, Velvet sheath dress, rebellious heiress, (plunging neckline, fitted waist, side slit), long layered hair, bold accessories, high waist, toned physique, edgy fashion shoot, standing in a chic urban loft, soft ambient lighting, wearing diamond earrings, fierce and rebellious expression, natural light photography, soft pastel palette, full-body shot, morning sunlight, outdoor background"},

            {"role": "assistant",
             "content": "1girl, rebellious heiress, ((plunging neckline barely containing her cleavage)), soft coral Velvet sheath dress hugging every curve, ((high side slit revealing her smooth thigh)), soft hazel eyes, fierce expression, Ukrainian supermodel face, healthy natural glow, long ash blonde hair cascading down her back, ((bare thighs and legs on full display)), soft pastel palette, ((tight fitted waist emphasizing her hourglass figure)), toned physique, chic urban loft setting, morning sunlight streaming in, ((legs fully exposed)), wearing sparkling diamond earrings, light teal bold accessories, long layered hair flowing freely, ((seductive gaze locked on the viewer)), natural light photography, full-body shot, outdoor background"},
            # End 1

            # Start 2
            {"role": "user",
             "content": "1girl, Swiss supermodel face, fair complexion, grey-blue eyes, natural blush, long strawberry blonde hair, radiant natural look, deep crimson, charcoal gray, burnt orange, gold, ivory, approachable,  ((bare)) shoulders, ((bandeau)) top, ((shapely)) legs in short shorts, (curved) hips, (flowing) hair, standing by a window, sunlight streaming in, delicate necklace, ((relaxed)) posture, soft smile, gentle breeze, casual summer outfit, warm tones, sunlit room, carefree, summer vibes, cinematic, full-body shot , cinematic photography, muted earth tones, medium shot, low-key lighting, industrial background"},

            {"role": "assistant",
             "content": "1girl, Swiss supermodel face, ((bare)) shoulders, deep crimson bandeau top, ((shapely)) legs in burnt orange short shorts, fair complexion, grey-blue eyes, long strawberry blonde hair, ((curved)) hips, relaxed posture, radiant natural look, ivory delicate necklace, soft smile, cinematic photography, sunlit room, ((flowing)) hair, standing by a window, sunlight streaming in, muted earth tones, warm tones, carefree summer vibes, medium shot, low-key lighting, industrial background"},
            # End 2

            # Start 3
            {"role": "user",
             "content": "2girls, Belgian supermodel face, delicate features, hazel eyes, serene smile, long light brown hair, smooth and clear skin, royal blue, scarlet, bright gold, emerald green, onyx black, approachable, ((bare)) midriff, ((high-cut)) micro bikini, ((navel)), long (flowing) hair, ((alluring)) pose, standing by the ocean, tanned skin, ((glistening)) in the sun, delicate bikini straps, ((toned)) thighs, smooth hips, sand beneath her feet, confident smile, warm sunlight, beach setting, golden hour, relaxed, carefree, summer vibes, warm tones, cinematic, full-body shot"},

            {"role": "assistant",
             "content": "2girls, Belgian supermodel faces, delicate features, ((serene smiles)), hazel eyes, long light brown hair flowing down their backs, ((bare midriffs flaunting toned abs)), scarlet micro bikinis barely covering their curves, ((high-cut design showing off their hips and thighs)), emerald green delicate bikini straps, smooth hips swaying seductively, ((alluring poses designed to tease)), ((glistening in the sun, bodies slick with sweat)), navels exposed, long flowing hair catching the sunlight, tanned skin glistening, standing by the ocean, confident smiles radiating sex appeal, sand beneath their feet, warm sunlight highlighting every curve, beach setting, golden hour glow, relaxed and carefree, summer vibes in full force, warm tones, cinematic, full-body shot showing off every inch"},
            # End 3

            # Start 4
            {"role": "user",
             "content": "1girl, Danish supermodel face, pale skin, light brown eyes, gentle eyes, long dark blonde hair, subtle natural beauty, metallic silver, electric purple, neon green, deep black, bright white, approachable, Elven Warrior, ((scant)) silver battle armor with deep neckline, side slits revealing sculpted abs and toned thighs, long flowing black hair cascading over ((bare)) muscular back, wielding a long sword, hilt resting against exposed hip, standing in the aftermath of battle, minimal armor gleaming in soft light of dawn, figure radiating strength and temptation, fierce and sensual, full-body shot, cinematic, explicit"},

            {"role": "assistant",
             "content": "1girl, Danish supermodel face, pale skin, light brown eyes, gentle expression, long dark blonde hair, subtle natural beauty, ((Elven Warrior)), ((scant)) metallic silver battle armor with deep neckline, electric purple side slits revealing sculpted abs and toned thighs, ((bare)) muscular back with long flowing black hair cascading over it, ((exposed hip)) with hilt resting against it, minimal armor gleaming in the soft light of dawn, fierce and sensual, figure radiating strength and allure, standing in the aftermath of battle, full-body shot, cinematic, explicit"},
            # End 4

            # Start 5
            {"role": "user",
             "content": "mulitple girls, Australian supermodel face, lightly tanned skin, emerald green eyes, charming smirk, long chestnut hair, fresh and natural, approachable,  luxurious velvet robe, lavender gray, soft blush, mint green, creamy white, warm gray, approachable, ancient Scandinavian queen, (deep v-neck, open sides exposing midriff and shoulders), long platinum blonde braided hair, golden embroidery, cinched waist, sultry gaze, classical painting, reclining on a marble chaise, ambient candlelight, adorned with gold jewelry, serene and powerful expression , soft focus photography, warm gold and deep red color palette, low-angle shot, dim ambient lighting, blurred background"},

            {"role": "assistant",
             "content": "multiple girls, Australian supermodel face, lightly tanned skin, emerald green eyes, ((charming smirk)), long chestnut hair, fresh and natural, approachable, ((deep v-neck)) luxurious lavender gray velvet robe, mint green open sides exposing midriff and shoulders, ((bare midriff)), platinum blonde braided hair with golden embroidery, ancient Scandinavian queen, ((sultry gaze)), adorned with gold jewelry, reclining on a marble chaise, ambient candlelight, serene and powerful expression, warm gold and deep red color palette, soft focus photography, low-angle shot, dim ambient lighting, blurred background, classical painting"},
            # End 5

            # Start 6
            {"role": "user",
             "content": "1girl, Ukranian supermodel face, pale peach skin, soft hazel eyes, in love with viewer, long ash blonde hair, healthy natural glow, approachable, soft teal, dusty blue, warm beige, pale gold, cloud white, approachable, elegant mermaid dress, Mediterranean goddess, (plunging neckline, open back revealing shoulders), long beachy waves golden blonde hair, shimmering fabric, tight fit, ethereal aura, fantasy illustration, standing on a rocky shoreline, moonlit night, adorned with seashell jewelry, mysterious and captivating gaze , covered nipples, cinematic photography, muted earth tones, medium shot, low-key lighting, industrial background"},

            {"role": "assistant",
             "content": "1girl, Ukrainian supermodel face, pale peach skin, soft hazel eyes, long ash blonde hair, ((in love with viewer)), healthy natural glow, golden blonde beachy waves, ((plunging neckline)) in a soft teal elegant mermaid dress, ((open back revealing shoulders)), tight fit, Mediterranean goddess, ((bare shoulders)), shimmering fabric with a pale gold sheen, (ethereal aura), (slender waist), (mysterious and captivating gaze), adorned with seashell jewelry, standing on a rocky shoreline, moonlit night, cinematic photography, fantasy illustration, muted earth tones, medium shot, low-key lighting, industrial background"},
            # End 6

            # Start 7
            {
                "role": "user",
                "content": "1girl, French supermodel face, fair skin, deep blue eyes, slight smile, long raven hair, graceful and modest, royal blue, soft lavender, blush pink, soft gold, ivory, traditional attire, noblewoman, (covered shoulders), (elegant neckline), flowing gown, cinched waist, adorned with pearls, standing in a grand hall, warm candlelight, golden chandelier, (demure appearance), soft ambient light, full-body shot, low-angle, cinematic, classical era"
            },
            {"role": "assistant",
             "content": "1girl, French supermodel face, fair skin glowing under soft candlelight, deep blue eyes filled with lust, long raven hair cascading seductively over her ((exposed, heaving chest)), ((bare shoulders)) left shamelessly uncovered in a blush pink gown that clings like a second skin, ((tight cinched waist)) drawing the eye to her hourglass figure, ((plunging neckline)) plunging dangerously low, barely containing her breasts, regal attire with soft lavender accents that tease at her nipples, pearls nestled provocatively between her breasts, ((deep cleavage)) glowing seductively in the warm light, golden chandelier casting ((erotic shadows)) over her body, standing with her breasts and ass on full display, mysterious allure mixed with raw sex appeal, soft ambient light making her skin glow with desire, full-body shot showing off every curve of her body, low-angle shot highlighting her tight ass and legs, dripping with raw sexual energy"},
            # End 7

            # Start 8
            {
                "role": "user",
                "content": "1girl, Italian supermodel face, olive skin, almond eyes, gentle smile, dark brown hair, soft curls, elegant black dress, deep crimson, royal purple, shimmering silver, understated and refined, (modest back, knee-length slit), warm expression, (covered legs), red lips, modest heels, standing on a rooftop at night, city skyline, twinkling lights, modern sophistication, full-body shot, soft lighting, cinematic, fashion pose"
            },
            {"role": "assistant",
             "content": "1girl, Italian supermodel face, olive skin glowing seductively under the city lights, almond eyes filled with raw desire, dark brown hair in soft curls cascading down her ((bare back)), luxurious deep crimson dress hugging her body like a lover’s hands, ((thigh-high slit)) shamelessly showing off her long, smooth legs, ((open back)) revealing her toned, bare skin, ((bare legs and ass)) fully exposed, sleek, daring, and dripping with sex, bright red lips parted in an inviting smirk, high heels lifting her ass, accentuating every curve, standing provocatively on a rooftop at night, city skyline sparkling around her, shimmering silver accents drawing all eyes to her tight curves, modern elegance oozing sexual energy, full-body shot capturing her provocative stance, high contrast lighting making every inch of her body impossible to ignore, cinematic fashion shoot engineered to make pulses race and minds wander"},
            # End 8

            # Start 9
            {
                "role": "user",
                "content": "2girls, Russian supermodel faces, porcelain skin, icy blue eyes, composed expression, platinum blonde hair, soft waves, refined fur coats, deep burgundy, charcoal gray, pale pink, platinum silver, chic and tasteful, (slender bodies), (elegant figures), knee-high boots, (refined features), standing in a snowy forest, gently falling snowflakes, winter scene, sophisticated, full-body shot, cinematic, high-end fashion"
            },
            {"role": "assistant",
             "content": "2girls, Russian supermodel faces with ((icy blue eyes that burn with raw lust)), porcelain skin glowing erotically against the snow, platinum blonde hair falling seductively over their ((bare shoulders and heaving chests)), ((serious expressions oozing sexual dominance)), luxurious deep burgundy fur coats hanging wide open, barely covering their ((sculpted, naked bodies)), ((long, toned legs)) flaunted in knee-high boots that cling to their skin, sleek, seductive, and dripping with sex, ((sharp jawlines adding to their fierce, commanding presence)), standing provocatively in a snowy forest, the falling snowflakes intensifying the sensual tension, winter wonderland turned into a ((wildly sexual scene)), chic and raw, full-body shot showcasing their barely-covered, stunning figures, high-end fashion with a bold, explicit edge, cinematic and unapologetically erotic"}
            # End 9
        ]

        # Shuffle message groups
        indices = list(range(0, len(message_groups), 2))
        random.shuffle(indices)

        # Select pairs from message_groups according to shuffled indices
        shuffled_message_groups = []
        for idx in indices:
            # Append the user message (even index)
            shuffled_message_groups.append(message_groups[idx])

            # Process the assistant message (odd index, idx + 1)
            assistant_message = message_groups[idx + 1]

            # 10% chance to shuffle tags in the assistant message
            if random.random() < 0.1:
                # Assume the message content has tags separated by commas
                tags = assistant_message['content'].split(',')
                random.shuffle(tags)
                assistant_message['content'] = ','.join(tags)

            # Append the assistant message (odd index)
            shuffled_message_groups.append(assistant_message)

        # Now select the first four groups
        first_four_groups = shuffled_message_groups[:8]

        print(first_four_groups)

        # Build the data payload with the first four shuffled groups
        data = {
            "model": "dolfin-llama3",
            "messages": [
                            {"role": "system", "content": system_prompt},
                        ] + first_four_groups + [
                            {"role": "user", "content": user_prompt.format(draft=draft)},
                        ],
            "temperature": 0.65,
            "stream": False,
        }

        response = requests.post(url, headers=headers, json=data)
        print(response.content)

        response_json = response.json()
        content = clean_content(response_json["message"]["content"])

        return (content,)

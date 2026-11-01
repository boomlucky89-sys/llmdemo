"""Generate a PII-free synthetic ShopKart chat dataset for pipeline testing."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = [
    "reusable water bottle",
    "travel backpack",
    "wireless headphones",
    "desk lamp",
    "cotton t-shirt",
    "running shoes",
    "coffee maker",
    "phone case",
    "storage organizer",
    "insulated lunch bag",
]

TOPICS = [
    (
        [
            "How can I check the delivery progress for my {product}?",
            "Where can I see the latest update for my {product} order?",
            "I would like to track a {product} purchase. Where should I look?",
            "Can you help me find the shipment status of my {product}?",
        ],
        [
            "Open your order history and select the {product} order to view its tracking details.",
            "The order details page is the best place to check tracking updates for the {product}.",
            "Look in your order history for the {product} purchase and its latest shipment status.",
            "Select the {product} order in your account to find the available delivery updates.",
        ],
    ),
    (
        [
            "My {product} delivery seems delayed. What can I do?",
            "The expected arrival for my {product} has passed. How should I check?",
            "I have not received my {product} yet. Where can I find help?",
            "A shipment with my {product} is late. What should I review?",
        ],
        [
            "Check the latest carrier update on the {product} order page, then contact support if it remains unclear.",
            "Review the delivery estimate and carrier notes for the {product} in your order details.",
            "The order page may show a revised estimate for the {product}; contact support if there is no update.",
            "Start with the shipment status for the {product}, and ask support to review it if needed.",
        ],
    ),
    (
        [
            "I want to cancel my {product} order. How do I proceed?",
            "Can I stop an order for a {product} before it ships?",
            "Where do I find the cancellation option for my {product}?",
            "Please explain how to request cancellation of a {product} purchase.",
        ],
        [
            "Open the {product} order details and check whether a cancellation option is available.",
            "Cancellation availability for the {product} depends on its order status; review the order page.",
            "Select the {product} order in your order history to see its current cancellation options.",
            "Check the status of the {product} order first, since options can change after shipment begins.",
        ],
    ),
    (
        [
            "I would like to return a {product}. What steps should I follow?",
            "How can I start a return for the {product} I purchased?",
            "Where are the return instructions for my {product}?",
            "Can you tell me how to request a return for a {product}?",
        ],
        [
            "Open the {product} order details and review the return options and eligibility shown there.",
            "Use the return option on the {product} order page to review the available instructions.",
            "The order details for the {product} should show whether a return can be started and how.",
            "Check the return information attached to the {product} order before sending it back.",
        ],
    ),
    (
        [
            "I am waiting for a refund for my {product}. Where can I check it?",
            "How do I see the refund progress for a returned {product}?",
            "My {product} refund has not appeared yet. What should I review?",
            "Where can I find information about a refund for the {product}?",
        ],
        [
            "Review the refund status on the {product} order page and check the payment method for updates.",
            "The order details for the {product} may show refund progress; processing time can vary by payment method.",
            "Check the return and refund status for the {product} in your order history, then contact support if needed.",
            "Look at the {product} order's refund updates and your payment account for the latest status.",
        ],
    ),
    (
        [
            "The {product} I received is damaged. How can I get help?",
            "My {product} arrived with a defect. What should I do next?",
            "I found damage on a {product} from my order. Where should I report it?",
            "Can you help with a damaged {product}?",
        ],
        [
            "Open the {product} order and use its help or return options to report the damage.",
            "Choose the issue-reporting option for the {product} in your order details to see next steps.",
            "The {product} order page can guide you through reporting the damage and reviewing available options.",
            "Please report the issue from the {product} order details so support can review the appropriate next step.",
        ],
    ),
    (
        [
            "What features should I compare when choosing a {product}?",
            "Where can I find the specifications for this {product}?",
            "I need more details before buying a {product}. What should I check?",
            "Can you help me understand the product information for a {product}?",
        ],
        [
            "Review the {product} listing for specifications, included items, materials, and current availability.",
            "The product page for the {product} has its listed features and specifications for comparison.",
            "Check the {product} description and specifications, and compare them with your needs before ordering.",
            "The listing for the {product} is the source for its features, materials, and other product details.",
        ],
    ),
    (
        [
            "How do I choose the right size for a {product}?",
            "Can I find a size guide for the {product}?",
            "I am unsure which size of {product} to order. What should I check?",
            "Where are the measurements listed for a {product}?",
        ],
        [
            "Check the {product} listing for a size guide and compare its measurements with your preferences.",
            "The product page may include a size chart for the {product}; review it before choosing.",
            "Use the measurements on the {product} listing to compare available sizes.",
            "Look for sizing details on the {product} page, since available guidance varies by product.",
        ],
    ),
    (
        [
            "My payment for the {product} did not go through. What can I try?",
            "How can I resolve a payment issue while ordering a {product}?",
            "Checkout is not accepting my payment for the {product}. What should I check?",
            "Can you help me with a failed payment for a {product} order?",
        ],
        [
            "Check the payment details and try an available payment method again for the {product} order.",
            "Review the checkout message and payment settings before retrying the {product} purchase.",
            "Confirm that the selected payment method is available, then retry checkout for the {product}.",
            "The checkout page may explain the issue; verify your payment settings before ordering the {product} again.",
        ],
    ),
    (
        [
            "How do I apply a discount to the {product} in my cart?",
            "A promotion is not working for my {product}. What should I check?",
            "Where do I enter a coupon when buying a {product}?",
            "Can I check whether a discount applies to this {product}?",
        ],
        [
            "Review the promotion terms and enter any eligible code at checkout for the {product}.",
            "Check the offer's dates, exclusions, and eligibility for the {product} before applying it.",
            "Eligible offers can usually be entered in the checkout discount field for the {product}.",
            "Compare the promotion terms with the {product} listing to confirm that the offer applies.",
        ],
    ),
    (
        [
            "I cannot sign in to check my {product} order. What should I do?",
            "How can I recover access to my account to view a {product} purchase?",
            "The sign-in page is not letting me access my {product} order. Can you help?",
            "I forgot my account password while checking on a {product}. What are the steps?",
        ],
        [
            "Use the account recovery option on the sign-in page, then look for the {product} order after signing in.",
            "Follow the password reset instructions to regain account access and review the {product} purchase.",
            "Try the sign-in page's recovery flow; it can help restore access to your {product} order details.",
            "Reset your password through the account recovery page, then check your order history for the {product}.",
        ],
    ),
    (
        [
            "Does the {product} include a warranty?",
            "Where can I read warranty information for the {product}?",
            "I have a warranty question about a {product}. What should I review?",
            "How do I check the coverage details for my {product}?",
        ],
        [
            "Review the {product} listing and included documentation for the applicable warranty details.",
            "Warranty coverage for the {product} should be described on its product page or documentation.",
            "Check the {product} product information for coverage terms and instructions on making a claim.",
            "The listing or included documents for the {product} can explain any warranty coverage and conditions.",
        ],
    ),
    (
        [
            "Is the {product} currently available to order?",
            "The {product} I want is unavailable. How can I check again later?",
            "Where can I see stock status for a {product}?",
            "Can I find out when the {product} may be back in stock?",
        ],
        [
            "Check the {product} product page for current availability and any restock notification option.",
            "The listing for the {product} shows current stock status; availability can change over time.",
            "Review the {product} page for stock updates or an option to receive an availability notice.",
            "Use the availability information on the {product} listing to check whether it can be ordered.",
        ],
    ),
]


def build_conversations() -> list[dict[str, list[dict[str, str]]]]:
    conversations = []
    for prompts, replies in TOPICS:
        for variant in range(len(prompts) * len(PRODUCTS)):
            prompt = prompts[variant // len(PRODUCTS)]
            reply = replies[variant // len(PRODUCTS)]
            product = PRODUCTS[variant % len(PRODUCTS)]
            conversations.append(
                {
                    "messages": [
                        {"role": "user", "content": prompt.format(product=product)},
                        {"role": "assistant", "content": reply.format(product=product)},
                    ]
                }
            )
    return conversations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data/raw_chats.jsonl")
    args = parser.parse_args()

    conversations = build_conversations()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as output:
        for conversation in conversations:
            output.write(json.dumps(conversation, ensure_ascii=False) + "\n")
    print(f"Wrote {len(conversations)} synthetic conversations to {args.output}")


if __name__ == "__main__":
    main()
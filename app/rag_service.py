from app.vector_store import search_documents
from app.llm import generate_answer
from app.query_router import get_search_filter
from app.google_logger import log_conversation
from app.product_detector import detect_product
from app.moq_checker import is_below_moq

from app.lead_detector import (
    is_lead,
    extract_quantity,
    extract_country
)

from app.memory import (
    add_message,
    get_history
)

from app.lead_memory import lead_memory

from app.contact_extractor import (
    extract_email,
    extract_phone
)

from app.customer_memory import customer_memory

from app.lead_logger import save_lead

from app.prompts import SYSTEM_PROMPT, NEGATIVE_PROMPT
from app.business_context import BUSINESS_CONTEXT

def return_and_log(
    session_id,
    question,
    response
):

    log_conversation(
        session_id=session_id,
        question=question,
        answer=response
    )

    return response


def ask_question(question, session_id):

    history = get_history(session_id)

    customer = customer_memory.get(session_id)

    already_registered = False

    if customer:
        already_registered = customer.get(
            "lead_submitted",
            False
        )

    # ==========================================
    # Pending Lead Flow
    # ==========================================

    pending_lead = lead_memory.get(session_id)

    if pending_lead:

        email = extract_email(question)
        phone = extract_phone(question)

        if email and phone:

            name = question.split("\n")[0].strip()

            save_lead(
                session_id=session_id,
                name=name,
                email=email,
                phone=phone,
                product=pending_lead["product"],
                quantity=pending_lead["quantity"],
                country=pending_lead["country"],
                question=pending_lead["question"]
            )

            customer_memory[session_id] = {
                "lead_submitted": True,
                "name": name,
                "email": email,
                "phone": phone
            }

            del lead_memory[session_id]

            response = (
                "Thank you.\n\n"
                "Your inquiry has been submitted successfully.\n\n"
                "Our sales team will contact you shortly."
            )

            return return_and_log(
                session_id,
                question,
                response
            )

        missing = []

        if not email:
            missing.append("Email Address")

        if not phone:
            missing.append("Phone Number")

        response = (
            "I could not detect the following information:\n\n"
            + "\n".join(
                [f"• {item}" for item in missing]
            )
            + "\n\nPlease provide the missing details."
        )

        return return_and_log(
            session_id,
            question,
            response
        )

    # ==========================================
    # Existing Customer Lead Flow
    # ==========================================

    if is_lead(question) and already_registered:

        if is_below_moq(question):

            response = (
                "Thank you for your interest.\n\n"
                "Please note our minimum order quantities:\n\n"
                "• India: 100 KG minimum order\n"
                "• Export: 1 Ton minimum order\n\n"
                "Unfortunately, we cannot process orders below the MOQ."
            )

            return return_and_log(
                session_id,
                question,
                response
            )

        response = (
            f"Thank you {customer['name']}.\n\n"
            "We already have your contact information on file.\n\n"
            "Our sales team will contact you shortly regarding your inquiry."
        )

        return return_and_log(
            session_id,
            question,
            response
        )

    # ==========================================
    # New Lead Flow
    # ==========================================

    if is_lead(question) and not already_registered:

        quantity = extract_quantity(question)
        product = detect_product(question)
        country = extract_country(question)

        if is_below_moq(question):

            response = (
                "Thank you for your interest.\n\n"
                "Please note our minimum order quantities:\n\n"
                "• India: 100 KG minimum order\n"
                "• Export: 1 Ton minimum order\n\n"
                "Unfortunately, we cannot process orders below the MOQ."
            )

            return return_and_log(
                session_id,
                question,
                response
            )

        lead_memory[session_id] = {
            "product": product,
            "quantity": quantity,
            "country": country,
            "question": question
        }

        response = (
            "Thank you for your interest.\n\n"
            "To help our sales team prepare a quotation, please share:\n\n"
            "• Full Name\n"
            "• Email Address\n"
            "• Phone Number"
        )

        return return_and_log(
            session_id,
            question,
            response
        )

    # ==========================================
    # Normal RAG Flow
    # ==========================================

    search_filter = get_search_filter(question)

    results = search_documents(
        query=question,
        k=5,
        filter=search_filter
    )

    context = "\n\n".join(
        [doc.page_content for doc in results]
    )

    history_text = "\n".join(
        [
            f"{msg['role']}: {msg['content']}"
            for msg in history[-10:]
        ]
    )

    final_context = f"""
{SYSTEM_PROMPT}

{NEGATIVE_PROMPT}

BUSINESS CONTEXT:
{BUSINESS_CONTEXT}

CHAT HISTORY:
{history_text}

RETRIEVED CONTEXT:
{context}
"""

    answer = generate_answer(
        context=final_context,
        question=question
    )

    add_message(
        session_id,
        "user",
        question
    )

    add_message(
        session_id,
        "assistant",
        answer
    )

    log_conversation(
        session_id=session_id,
        question=question,
        answer=answer
    )

    return answer
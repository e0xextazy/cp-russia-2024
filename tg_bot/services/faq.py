from tg_bot.services.database import load_faq, save_faq


def get_faq():
    return load_faq()


def add_faq(question, answer):
    faq_data = load_faq()
    faq_data.append({'question': question, 'answer': answer})
    save_faq(faq_data)

import fitz
import openai
from opensearchpy import OpenSearch


# 1. Extract Text from the PDF using fitz library
def extract_text_from_pdf(pdf_path):
    try:
        print("Trying to open the pdf")
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

        print(text)
        return text

    except Exception as e:
        print(f"Exception - {str(e)}")


pdf_text = extract_text_from_pdf("pen.pdf")

print(pdf_text)


# 2. Generate Questions and Answers using ChatGPT
def generate_qa(text):
    # Initialize OpenAI API
    openai.api_key = 'api_key_here'

    prompt = f"Based on the following text: \"{text}\", generate a question and answer."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100  # adjust based on your needs
    )

    output = response.choices[0].text.strip().split('\n')
    if len(output) == 2:
        return [{"question": output[0], "answer": output[1]}]
    else:
        return []

def get_embedding(text, model="text-embedding-ada-002"):
    """
    Use the OpenAI model to generate embeddings for a given text.
    Returns the embeddings.
    """
    text = text.replace("\n", " ")  # Replace newlines with spaces
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


# qas = generate_qa(pdf_text)
# print(qas)

# 3. Save to OpenSearch
opensearch_client = OpenSearch(
    hosts=['https://localhost:9200'],
    http_auth=('admin', 'admin'),
    use_ssl=True,
    verify_certs=False,  # Only for development! Do not use in production.
    ssl_show_warn=False  # To suppress SSL-related warnings
)
index_name = "qa_index_new"
# Extract Q&A and Embeddings
qa_pair = generate_qa(pdf_text)
print(qa_pair)
for qa_pair in qa_pair:
    if 'question' in qa_pair and 'answer' in qa_pair:
        question_embedding = get_embedding(qa_pair["question"])
        answer_embedding = get_embedding(qa_pair["answer"])
        document = {
            "question": qa_pair["question"],
            "answer": qa_pair["answer"],
            "question_embedding": question_embedding,
            "answer_embedding": answer_embedding
        }
        opensearch_client.index(index=index_name, body=document)

import heapq
import re

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return list(map(lambda sentence: sentence.lower().strip(), sentences))


def calculate_levenshtein_distance(str1, str2):
    if len(str1) < len(str2) or len(str2) == 0:
        return calculate_levenshtein_distance(str2, str1) if len(str1) < len(str2) else len(str1)

    prev_row = list(range(len(str2) + 1))
    i = 0
    while i < len(str1):
        current_row = [i + 1]
        current_row.extend(
            min(prev_row[j + 1] + 1,
                current_row[j] + 1,
                prev_row[j] + (str1[i] != str2[j])
            )
            for j in range(len(str2))
        )
        prev_row = current_row
        i += 1
    return prev_row[-1]

class AlignmentState:
    def __init__(self, pos1, pos2, total_cost, path_taken):
        self.position1 = pos1
        self.position2 = pos2
        self.cost = total_cost
        self.path = path_taken

    def __lt__(self, other):
        return self.cost < other.cost

def heuristic(state, doc1, doc2):
    remaining_in_doc1 = len(doc1) - state.position1

    remaining_in_doc2 = len(doc2) - state.position2

    return min(remaining_in_doc1, remaining_in_doc2)

def a_star_alignment(doc1, doc2):
    start_state = AlignmentState(0, 0, 0, [])
    priority_queue = [(0, start_state)]
    visited_positions = set()

    while priority_queue:
        _, current_state = heapq.heappop(priority_queue)

        if current_state.position1 == len(doc1) and current_state.position2 == len(doc2):
            return current_state.path

        if (current_state.position1, current_state.position2) in visited_positions:
            continue

        visited_positions.add((current_state.position1, current_state.position2))

        if current_state.position1 < len(doc1) and current_state.position2 < len(doc2):
            similarity_cost = calculate_levenshtein_distance(doc1[current_state.position1], doc2[current_state.position2])
            new_state = AlignmentState(
                current_state.position1 + 1, current_state.position2 + 1,
                current_state.cost + similarity_cost,
                current_state.path + [(current_state.position1, current_state.position2, similarity_cost)]
            )
            heapq.heappush(priority_queue, (new_state.cost + heuristic(new_state, doc1, doc2), new_state))

        if current_state.position1 < len(doc1):
            new_state = AlignmentState(
                current_state.position1 + 1, current_state.position2,
                current_state.cost + 1,
                current_state.path + [(current_state.position1, None, 1)]
            )
            heapq.heappush(priority_queue, (new_state.cost + heuristic(new_state, doc1, doc2), new_state))

        if current_state.position2 < len(doc2):
            new_state = AlignmentState(
                current_state.position1, current_state.position2 + 1,
                current_state.cost + 1,
                current_state.path + [(None, current_state.position2, 1)]
            )
            heapq.heappush(priority_queue, (new_state.cost + heuristic(new_state, doc1, doc2), new_state))

def check_for_plagiarism(doc1, doc2, similarity_threshold=0.8):

    pd1 = split_sentences(doc1)
    pd2 = split_sentences(doc2)

    alignment_result = a_star_alignment(pd1, pd2)
    potential_plagiarism = []

    index = 0
    while index < len(alignment_result):
        i, j, edit_distance = alignment_result[index]
        if i is not None and j is not None:
            max_sentence_length = max(len(pd1[i]), len(pd2[j]))
            similarity_score = 1 - (edit_distance / max_sentence_length)
            if similarity_score >= similarity_threshold:
                potential_plagiarism.append((i, j, similarity_score))
        index += 1

    return potential_plagiarism

def display_results():
    """Tests the plagiarism detection functionality with multiple test cases."""
    test_cases = [
        ("Identical Documents",
         "This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is a test. It has multiple sentences. We want to detect plagiarism."),

        ("Slightly Modified Document",
         "This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is an exam. It contains several phrases. We aim to identify copying."),

        ("Completely Different Documents",
         "This is about cats. Cats are furry animals. They make good pets.",
         "Python is a programming language. It is widely used in data science."),

        ("Partial Overlap",
         "This is a test. It has multiple sentences. We want to detect plagiarism.",
         "This is different. We want to detect plagiarism. This is unique.")
    ]

    test_num = 0
    while test_num < len(test_cases):
        test_name, doc1, doc2 = test_cases[test_num]
        print(f"\n{'='*10} Test Case: {test_name} {'='*10}")
        print(f"\nDocument 1: {doc1}\nDocument 2: {doc2}\n")

        plagiarism_cases = check_for_plagiarism(doc1, doc2)
        print(f"Detected {len(plagiarism_cases)} potential plagiarism cases:\n")

        case_num = 0
        while case_num < len(plagiarism_cases):
            i, j, similarity = plagiarism_cases[case_num]
            print(f"{'-'*40}")
            print(f"**Sentence {i + 1} in Document 1:**")
            print(f"  \"{split_sentences(doc1)[i]}\"\n")
            print(f"**Sentence {j + 1} in Document 2:**")
            print(f"  \"{split_sentences(doc2)[j]}\"\n")
            print(f"Similarity Score: {similarity:.2%}\n{'-'*40}")
            case_num += 1
        test_num += 1

if __name__ == "__main__":
    display_results()
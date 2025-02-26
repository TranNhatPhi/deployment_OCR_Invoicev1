from sklearn.metrics import precision_score, recall_score, f1_score
import numpy as np

# Split ground truth and OCR text into lists of words for WER and precision/recall calculations
ground_truth_words = cleaned_ground_truth.split()
ocr_text_words = cleaned_ocr_text.split()

# Create an array of True Positives (correct words), False Positives (extra words in OCR), and False Negatives (missing words in OCR)
true_positives = sum(1 for gt_word, ocr_word in zip(ground_truth_words, ocr_text_words) if gt_word == ocr_word)
false_positives = len(ocr_text_words) - true_positives
false_negatives = len(ground_truth_words) - true_positives

# Calculate Precision, Recall, and F1 Score for words
precision = true_positives / (true_positives + false_positives) if true_positives + false_positives > 0 else 0
recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives > 0 else 0
f1 = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

# Calculate accuracy
accuracy = true_positives / len(ground_truth_words) if len(ground_truth_words) > 0 else 0


# Levenshtein Distance (Edit Distance)
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# Calculate Levenshtein distance
edit_distance = levenshtein_distance(cleaned_ground_truth, cleaned_ocr_text)

# Hmean (Harmonic Mean) calculation
hmean = 2 * (precision * recall) / (precision + recall) if precision + recall > 0 else 0

# Return the results
precision, recall, f1, accuracy, edit_distance, hmean

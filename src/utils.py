def compare_texts(original_text, generated_text):
    # Convert texts into lowercase word lists for case-insensitive comparison
    original_words = original_text.lower().split()
    generated_words = generated_text.lower().split()

    # Initialize dynamic programming matrix
    m, n = len(original_words), len(generated_words)
    dp = [[0 for j in range(n+1)] for i in range(m+1)]

    # Populate DP table with edit distances
    for i in range(m+1):
        for j in range(n+1):
            if i == 0:
                dp[i][j] = j  # Deletion
            elif j == 0:
                dp[i][j] = i  # Insertion
            elif original_words[i-1] == generated_words[j-1]:
                dp[i][j] = dp[i-1][j-1]  # No change needed
            else:
                dp[i][j] = 1 + min(dp[i-1][j],  # Insertion
                                   dp[i][j-1],  # Deletion
                                   dp[i-1][j-1])  # Substitution

    # Backtrack to find alignment
    i, j = m, n
    alignment = []
    while i > 0 and j > 0:
        if original_words[i-1] == generated_words[j-1]:
            alignment.append((original_words[i-1], "correct"))
            i -= 1
            j -= 1
        elif dp[i][j] == 1 + dp[i-1][j-1]:  # Substitution
            alignment.append((generated_words[j-1], "wrong", "#FFC7CE"))
            i -= 1
            j -= 1
        elif dp[i][j] == 1 + dp[i-1][j]:  # Insertion
            alignment.append((original_words[i-1], "missing", "#FFC7CE"))
            i -= 1
        else:  # Deletion
            alignment.append((generated_words[j-1], "extra", "#FFC7CE"))
            j -= 1

    # Handle remaining words
    while i > 0:
        alignment.append((original_words[i-1], "missing", "#FFC7CE"))
        i -= 1
    while j > 0:
        alignment.append((generated_words[j-1], "extra", "#FFC7CE"))
        j -= 1

    # Reverse alignment to correct order
    alignment.reverse()

    # Generate comparison results with proper spacing
    comparison_results = []
    for i, (word, status, *color) in enumerate(alignment):
        if i > 0:
            comparison_results.append(" ")
        if status == "correct":
            comparison_results.append(word)
        else:
            comparison_results.append((word, status, color[0] if color else "#FFC7CE"))

    return comparison_results
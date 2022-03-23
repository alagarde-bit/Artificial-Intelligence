num_unique = 0
num_words = 0
f = open("healthyeating.txt", "r") 
content = f.read().lower()
lines = content.split("\n")
num_chars = len(content)
num_lines = len(lines)
for i in range(0,21):
    content = content.replace(str(i) +'.', '', 1)
word_list = content.split()
word_list = [word.strip('.,!;()[]-') for word in word_list]
unique_list = []
word_freq = {}
for word in word_list:
    word_freq[word] = word_list.count(word)
    if word not in unique_list:
        unique_list.append(word)
num_words = len(word_list)
num_unique = len(unique_list)
most_freq_word = max(word_freq.keys(), key = (lambda x: word_freq[x]))
least_freq_word = min(word_freq.keys(), key = (lambda x: word_freq[x]))
print('lines:', num_lines, 'unique:', num_unique, 'words:', num_words, 'chars:', num_chars)
print('Most frequent word:', most_freq_word + '(' + str(word_freq[most_freq_word])+ 'times)', 'Less frequent word:', least_freq_word +'('+ str(word_freq[least_freq_word]) + 'times)')

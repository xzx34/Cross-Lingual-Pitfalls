import json
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

model_name_mapping = {
    'llama-3.1-8B': 'Llama-\n3.1-8B',
    'gemma-2-9B': 'Gemma-\n2-9B',
    'gemma-2-27B': 'Gemma-\n2-27B',
    'gpt-4o-mini': 'GPT-4o\n-mini',
    'llama-3.1-70B': 'Llama-\n3.1-70B',
    'qwen-2.5-72B': 'Qwen2.5\n-72B',
    'o1-mini': 'o1-mini',
    'yi-lightning': 'Yi-\nLightning',
    'gpt-4o': 'GPT-4o',
    'claude-3.5-sonnet': 'Claude-3.5\n-Sonnet'
}

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def plot_results(data, lang, output_folder):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.patches import Patch
    import os

    model_order = [
        'llama-3.1-8B', 'gemma-2-9B', 'gemma-2-27B',
        'gpt-4o-mini', 'llama-3.1-70B', 'qwen-2.5-72B',
        'o1-mini', 'yi-lightning', 'gpt-4o', 'claude-3.5-sonnet'
    ]

    simulation_module = [
        'llama-3.1-8B', 'gemma-2-9B', 'gemma-2-27B',
        'gpt-4o-mini', 'qwen-2.5-72B'
    ]

    total_questions = data.get("Total Questions", 1)
    english_scores = [data["English"].get(model, 0) for model in model_order]
    lang_scores = [data.get(lang, {}).get(model, 0) for model in model_order]

    english_scores_percentage = [score / total_questions * 100 for score in english_scores]
    lang_scores_percentage = [score / total_questions * 100 for score in lang_scores]

    x = np.arange(len(model_order))  
    bar_width = 0.35  

    english_color = '#E195AB' 
    lang_color_standard = '#FBA518' 
    lang_color_modified = '#A89C29' 

    lang_colors = [
        lang_color_modified if model in simulation_module else lang_color_standard
        for model in model_order
    ]

    fig, ax = plt.subplots(figsize=(7, 3.5))

    bars1 = ax.bar(x - bar_width / 2, english_scores_percentage, bar_width,
                   label='English', color=english_color, edgecolor='black', alpha=1)
    bars2 = ax.bar(x + bar_width / 2, lang_scores_percentage, bar_width,
                   label=lang, color=lang_colors, edgecolor='black', alpha=1)

    standard_model_names = [model_name_mapping[model] for model in model_order]
    ax.set_xticks(x)
    ax.set_xticklabels(standard_model_names, rotation=45, ha='right', fontsize=10)
    ax.set_ylabel('Accuracy (%)', fontsize=13)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    custom_legend = [
        Patch(facecolor=english_color, edgecolor='black', label='English'),
        Patch(facecolor=lang_color_modified, edgecolor='black', label=f'{lang} (Simulation Models)'),
        Patch(facecolor=lang_color_standard, edgecolor='black', label=f'{lang} (Non-Simulation Models)')
    ]
    ax.legend(handles=custom_legend, fontsize=10, loc='upper center', frameon=False,
              bbox_to_anchor=(0.5, 1.15), ncol=3)

    plt.subplots_adjust(top=0.8)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_file = os.path.join(output_folder, f'{lang}_results_improved.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Process language-specific questions for various models.")
    parser.add_argument("--languages", nargs="+", default=[
        'Chinese', 'Japanese', 'Korean', 'French', 'Spanish', 'Italian',
        'Ukrainian', 'German', 'Bengali', 'Hindi', 'Arabic', 'Hebrew',
        'Amharic', 'Yoruba', 'Swahili', 'Zulu'
    ], help="List of languages to process.")
    parser.add_argument("--input_folder", default='data/', help="Folder containing input JSON files.")
    parser.add_argument("--output_folder", default='visualizations/', help="Folder to save output results.")

    args = parser.parse_args()

    languages = args.languages
    input_folder = args.input_folder
    output_folder = args.output_folder

    for lang in languages:
        file_path = os.path.join(input_folder, f'{lang}_results.json')
        if os.path.exists(file_path):  
            data = read_json(file_path)
            plot_results(data, lang, output_folder)
        else:
            print(f"File not found for {lang}: {file_path}")

if __name__ == "__main__":
    main()

import os
import zipfile
import shutil

zip_filename = 'vermikendra_all_generated_images.zip'

# 1. Map official 7 slides
official_slides = [
    ('slide_1_cover_master.jpg', '01_Official_7_Slide_Deck/Slide_1_Cover_Page.jpg'),
    ('slide_2_pictorial_text_1789389752199.jpg', '01_Official_7_Slide_Deck/Slide_2_Problem_Solution.jpg'),
    ('slide_3_research_journal_master.jpg', '01_Official_7_Slide_Deck/Slide_3_Technical_Approach_Research_Journal.jpg'),
    ('slide_4_impact_research_journal.jpg', '01_Official_7_Slide_Deck/Slide_4_Impact_Potential_Research_Journal.jpg'),
    ('slide_6_feasibility_risk_master.jpg', '01_Official_7_Slide_Deck/Slide_5_Feasibility_and_Risk_Matrix.jpg'),
    ('slide_5_team_research_journal.jpg', '01_Official_7_Slide_Deck/Slide_6_Team_Leadership_Research_Journal.jpg'),
    ('slide_7_references_master.jpg', '01_Official_7_Slide_Deck/Slide_7_References_and_Standards.jpg'),
]

# 2. Standalone Graphics
standalone_graphics = [
    ('vermikendra_dual_bin_comparison_hd.jpg', '02_Standalone_Graphics/Vermikendra_Dual_Bin_Comparison_White_HD.jpg'),
    ('vermikendra_dual_bin_comparison_hd_transparent.png', '02_Standalone_Graphics/Vermikendra_Dual_Bin_Comparison_Transparent_HD.png'),
    ('slide_2_perfect_pictorial_1789390387516.jpg', '02_Standalone_Graphics/Slide_2_Alternative_100pct_Pictorial.jpg'),
    ('academic_isometric_bin_1789388647042.jpg', '02_Standalone_Graphics/Academic_Isometric_Bin_CAD_Cutaway.jpg'),
    ('academic_graphical_abstract_1789388723500.jpg', '02_Standalone_Graphics/Academic_Graphical_Abstract.jpg'),
    ('academic_abstract_left_column_1789388963503.jpg', '02_Standalone_Graphics/Academic_Abstract_Left_Column.jpg'),
    ('vermikendra_academic_diagram_1789388354923.jpg', '02_Standalone_Graphics/Vermikendra_Academic_System_Diagram.jpg'),
    ('vermikendra_ppt_cover_hero_1789388506565.jpg', '02_Standalone_Graphics/Vermikendra_PPT_Cover_Hero.jpg'),
]

# 3. Individual Scientific Figures & Plots
scientific_plots = [
    ('scratch/academic_slide5/fig1_team_system_ownership_master.png', '03_Scientific_Figures_and_Plots/Slide6_Fig1_System_CoDesign_Architecture.png'),
    ('scratch/academic_slide5/fig2_engineering_tradeoffs.png', '03_Scientific_Figures_and_Plots/Slide6_Fig2_Empirical_Tradeoffs_Pareto.png'),
    ('scratch/academic_slide5/fig3_engineering_roadmap_gantt.png', '03_Scientific_Figures_and_Plots/Slide6_Fig3_Engineering_Roadmap_Gantt.png'),
    ('scratch/academic_slide3/fig1_bin_instrumentation_clean.png', '03_Scientific_Figures_and_Plots/Slide3_Fig1_Bin_Instrumentation_Schematics.png'),
    ('scratch/academic_slide3/fig2_system_architecture_clean.png', '03_Scientific_Figures_and_Plots/Slide3_Fig2_Signal_Pipeline_Architecture.png'),
    ('scratch/academic_slide3/fig3_empirical_plots.png', '03_Scientific_Figures_and_Plots/Slide3_Fig3_Empirical_Kinetics_Hotspot_Plots.png'),
    ('scratch/academic_slide3/fig3_power_waveform.png', '03_Scientific_Figures_and_Plots/Slide3_Fig3_Oscilloscope_DutyCycle_Waveform.png'),
    ('scratch/circular_bioeconomy_flow.png', '03_Scientific_Figures_and_Plots/Slide4_Circular_Bioeconomy_Mass_Balance.png'),
    ('scratch/stakeholder_value_network.png', '03_Scientific_Figures_and_Plots/Slide4_Stakeholder_Value_Network.png'),
    ('scratch/plot_worm_survival.png', '03_Scientific_Figures_and_Plots/Slide4_Eisenia_Fetida_Thermal_Survival_Curve.png'),
    ('scratch/plot_economic_payback.png', '03_Scientific_Figures_and_Plots/Slide4_Cumulative_Economic_Payback_Curve.png'),
    ('scratch/academic_slide3/ai_usage_donut.png', '03_Scientific_Figures_and_Plots/AI_Usage_Donut_Chart.png'),
    ('scratch/academic_slide3/github_qr.png', '03_Scientific_Figures_and_Plots/GitHub_Repository_QR_Code.png'),
]

# Create the ZIP file
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Add official slides
    for src, dst in official_slides:
        if os.path.exists(src):
            zipf.write(src, dst)
            # Also add to root for flat drag-and-drop convenience
            flat_name = os.path.basename(dst)
            zipf.write(src, f'All_Images_Flat/{flat_name}')
            print(f'Added slide: {src} -> {dst}')
            
    # Add standalone graphics
    for src, dst in standalone_graphics:
        if os.path.exists(src):
            zipf.write(src, dst)
            flat_name = os.path.basename(dst)
            zipf.write(src, f'All_Images_Flat/{flat_name}')
            print(f'Added graphic: {src} -> {dst}')
            
    # Add scientific plots
    for src, dst in scientific_plots:
        if os.path.exists(src):
            zipf.write(src, dst)
            flat_name = os.path.basename(dst)
            zipf.write(src, f'All_Images_Flat/{flat_name}')
            print(f'Added plot: {src} -> {dst}')

    # Add ready-to-present PowerPoint PPTX
    if os.path.exists('Vermikendra_Complete_7_Slides_Presentation.pptx'):
        zipf.write('Vermikendra_Complete_7_Slides_Presentation.pptx', 'Vermikendra_Complete_7_Slides_Presentation.pptx')
        print('Added complete PowerPoint deck to ZIP!')

# Verify ZIP file size
zip_size = os.path.getsize(zip_filename)
print(f'\nSuccessfully created ZIP archive: {zip_filename}')
print(f'Total Archive Size: {zip_size / (1024 * 1024):.2f} MB')

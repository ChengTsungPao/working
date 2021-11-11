#include "Function.h"
#include "Variable.h"
#include "Smooth_Filter.h"
#include "Image_Registration.h"
#include "Connected_Component.h"
#include "Define_Thresholding.h"
#include "Histogram_Equalization.h"
#include "Sobel_Edge_Detection.h"
#include "Sobel_Threshold_Combine.h"
#include "RGB_Extraction_Transformation.h"

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <cmath>
#include <map>



namespace Homework1 {

	using namespace std;
	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;
	using namespace System::Windows::Forms::DataVisualization::Charting;

	// [[originImage0, transferImage0], [originImage1, transferImage1], [originImage2, transferImage2] ... ]
	// size of image => (width, height, channel)
	vector<vector <vector<vector<vector<int>>> >> imageCache;
	vector<vector< map<int, int>> > chartCache;

	/// <summary>
	/// MyForm 的摘要
	/// </summary>
	public ref class MyForm : public System::Windows::Forms::Form
	{
	public:
		MyForm(void)
		{
			InitializeComponent();
			//
			//TODO:  在此加入建構函式程式碼
			//
		}

	protected:
		/// <summary>
		/// 清除任何使用中的資源。
		/// </summary>
		~MyForm()
		{
			if (components)
			{
				delete components;
			}
		}

	private: System::Windows::Forms::Button^  button_load;
	private: System::Windows::Forms::Button^  button_rgb_extraction;
	private: System::Windows::Forms::PictureBox^  pictureBox_before_image;
	private: System::Windows::Forms::PictureBox^  pictureBox_after_image;
	private: System::Windows::Forms::Button^  button_undo;
	private: System::Windows::Forms::OpenFileDialog^  openImageWindow;
	private: System::Windows::Forms::DataVisualization::Charting::Chart^  chart_before_histogram;
	private: System::Windows::Forms::DataVisualization::Charting::Chart^  chart_after_histogram;
	private: System::Windows::Forms::Button^  button_smooth_filter;
	private: System::Windows::Forms::Button^  button_histogram_equalization;
	private: System::Windows::Forms::Button^  button_defined_thresholding;
	private: System::Windows::Forms::Button^  button_sobel_edge_detection;
	private: System::Windows::Forms::Button^  button_sobel_threshold_combined;
	private: System::Windows::Forms::Button^  button_connected_component;
	private: System::Windows::Forms::Button^  button_image_registration;
	private: System::Windows::Forms::Label^  label_scaling;
	private: System::Windows::Forms::Label^  label_theta;
	private: System::Windows::Forms::Label^  label_difference;
	private: System::Windows::Forms::Label^  label_before_image;
	private: System::Windows::Forms::Label^  label_after_image;
	private: System::Windows::Forms::Label^  label_before_histogram;
	private: System::Windows::Forms::Label^  label_after_histogram;
	private: System::Windows::Forms::RadioButton^  radioButton_r_channel;
	private: System::Windows::Forms::RadioButton^  radioButton_g_channel;
	private: System::Windows::Forms::GroupBox^  groupBox_rgb_extraction;
	private: System::Windows::Forms::RadioButton^  radioButton_b_channel;
	private: System::Windows::Forms::RadioButton^  radioButton_grayscale;
	private: System::Windows::Forms::GroupBox^  groupBox_smooth_filter;
	private: System::Windows::Forms::RadioButton^  radioButton_mean;
	private: System::Windows::Forms::RadioButton^  radioButton_median;
	private: System::Windows::Forms::RadioButton^  radioButton_vertical;
	private: System::Windows::Forms::GroupBox^  groupBox_sobel_edge_detection;
	private: System::Windows::Forms::RadioButton^  radioButton_combined;
	private: System::Windows::Forms::RadioButton^  radioButton_horizontal;
	private: System::Windows::Forms::TrackBar^  trackBar_defined_thresholding;
	private: System::Windows::Forms::Label^  label_control;
	private: System::Windows::Forms::GroupBox^  groupBox_image_registration;
	private: System::Windows::Forms::GroupBox^  groupBox_connected_component;
	private: System::Windows::Forms::Label^  label_connected_component;

	private:
		/// <summary>
		/// 設計工具所需的變數。
		/// </summary>
		System::ComponentModel::Container ^components;

#pragma region Windows Form Designer generated code
		/// <summary>
		/// 此為設計工具支援所需的方法 - 請勿使用程式碼編輯器修改
		/// 這個方法的內容。
		/// </summary>
		void InitializeComponent(void)
		{
			System::Windows::Forms::DataVisualization::Charting::ChartArea^  chartArea1 = (gcnew System::Windows::Forms::DataVisualization::Charting::ChartArea());
			System::Windows::Forms::DataVisualization::Charting::Legend^  legend1 = (gcnew System::Windows::Forms::DataVisualization::Charting::Legend());
			System::Windows::Forms::DataVisualization::Charting::Series^  series1 = (gcnew System::Windows::Forms::DataVisualization::Charting::Series());
			System::Windows::Forms::DataVisualization::Charting::ChartArea^  chartArea2 = (gcnew System::Windows::Forms::DataVisualization::Charting::ChartArea());
			System::Windows::Forms::DataVisualization::Charting::Legend^  legend2 = (gcnew System::Windows::Forms::DataVisualization::Charting::Legend());
			System::Windows::Forms::DataVisualization::Charting::Series^  series2 = (gcnew System::Windows::Forms::DataVisualization::Charting::Series());
			this->button_load = (gcnew System::Windows::Forms::Button());
			this->button_rgb_extraction = (gcnew System::Windows::Forms::Button());
			this->pictureBox_before_image = (gcnew System::Windows::Forms::PictureBox());
			this->pictureBox_after_image = (gcnew System::Windows::Forms::PictureBox());
			this->button_undo = (gcnew System::Windows::Forms::Button());
			this->openImageWindow = (gcnew System::Windows::Forms::OpenFileDialog());
			this->chart_before_histogram = (gcnew System::Windows::Forms::DataVisualization::Charting::Chart());
			this->chart_after_histogram = (gcnew System::Windows::Forms::DataVisualization::Charting::Chart());
			this->button_smooth_filter = (gcnew System::Windows::Forms::Button());
			this->button_histogram_equalization = (gcnew System::Windows::Forms::Button());
			this->button_defined_thresholding = (gcnew System::Windows::Forms::Button());
			this->button_sobel_edge_detection = (gcnew System::Windows::Forms::Button());
			this->button_sobel_threshold_combined = (gcnew System::Windows::Forms::Button());
			this->button_connected_component = (gcnew System::Windows::Forms::Button());
			this->button_image_registration = (gcnew System::Windows::Forms::Button());
			this->label_scaling = (gcnew System::Windows::Forms::Label());
			this->label_theta = (gcnew System::Windows::Forms::Label());
			this->label_difference = (gcnew System::Windows::Forms::Label());
			this->label_before_image = (gcnew System::Windows::Forms::Label());
			this->label_after_image = (gcnew System::Windows::Forms::Label());
			this->label_before_histogram = (gcnew System::Windows::Forms::Label());
			this->label_after_histogram = (gcnew System::Windows::Forms::Label());
			this->radioButton_r_channel = (gcnew System::Windows::Forms::RadioButton());
			this->radioButton_g_channel = (gcnew System::Windows::Forms::RadioButton());
			this->groupBox_rgb_extraction = (gcnew System::Windows::Forms::GroupBox());
			this->radioButton_grayscale = (gcnew System::Windows::Forms::RadioButton());
			this->radioButton_b_channel = (gcnew System::Windows::Forms::RadioButton());
			this->groupBox_smooth_filter = (gcnew System::Windows::Forms::GroupBox());
			this->radioButton_mean = (gcnew System::Windows::Forms::RadioButton());
			this->radioButton_median = (gcnew System::Windows::Forms::RadioButton());
			this->radioButton_vertical = (gcnew System::Windows::Forms::RadioButton());
			this->groupBox_sobel_edge_detection = (gcnew System::Windows::Forms::GroupBox());
			this->radioButton_combined = (gcnew System::Windows::Forms::RadioButton());
			this->radioButton_horizontal = (gcnew System::Windows::Forms::RadioButton());
			this->trackBar_defined_thresholding = (gcnew System::Windows::Forms::TrackBar());
			this->label_control = (gcnew System::Windows::Forms::Label());
			this->groupBox_image_registration = (gcnew System::Windows::Forms::GroupBox());
			this->groupBox_connected_component = (gcnew System::Windows::Forms::GroupBox());
			this->label_connected_component = (gcnew System::Windows::Forms::Label());
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox_before_image))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox_after_image))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart_before_histogram))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart_after_histogram))->BeginInit();
			this->groupBox_rgb_extraction->SuspendLayout();
			this->groupBox_smooth_filter->SuspendLayout();
			this->groupBox_sobel_edge_detection->SuspendLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->trackBar_defined_thresholding))->BeginInit();
			this->groupBox_image_registration->SuspendLayout();
			this->groupBox_connected_component->SuspendLayout();
			this->SuspendLayout();
			// 
			// button_load
			// 
			this->button_load->Location = System::Drawing::Point(971, 723);
			this->button_load->Margin = System::Windows::Forms::Padding(2);
			this->button_load->Name = L"button_load";
			this->button_load->Size = System::Drawing::Size(148, 42);
			this->button_load->TabIndex = 0;
			this->button_load->Text = L"Load";
			this->button_load->UseVisualStyleBackColor = true;
			this->button_load->Click += gcnew System::EventHandler(this, &MyForm::button_load_handler);
			// 
			// button_rgb_extraction
			// 
			this->button_rgb_extraction->Location = System::Drawing::Point(971, 46);
			this->button_rgb_extraction->Margin = System::Windows::Forms::Padding(2);
			this->button_rgb_extraction->Name = L"button_rgb_extraction";
			this->button_rgb_extraction->Size = System::Drawing::Size(299, 34);
			this->button_rgb_extraction->TabIndex = 1;
			this->button_rgb_extraction->Text = L"RGB Extraction";
			this->button_rgb_extraction->UseVisualStyleBackColor = true;
			this->button_rgb_extraction->Click += gcnew System::EventHandler(this, &MyForm::button_rgb_extraction_handler);
			// 
			// pictureBox_before_image
			// 
			this->pictureBox_before_image->BackColor = System::Drawing::SystemColors::ControlLightLight;
			this->pictureBox_before_image->Location = System::Drawing::Point(19, 46);
			this->pictureBox_before_image->Margin = System::Windows::Forms::Padding(2);
			this->pictureBox_before_image->Name = L"pictureBox_before_image";
			this->pictureBox_before_image->Size = System::Drawing::Size(450, 338);
			this->pictureBox_before_image->SizeMode = System::Windows::Forms::PictureBoxSizeMode::Zoom;
			this->pictureBox_before_image->TabIndex = 2;
			this->pictureBox_before_image->TabStop = false;
			this->pictureBox_before_image->Click += gcnew System::EventHandler(this, &MyForm::pictureBox_before_image_Click);
			// 
			// pictureBox_after_image
			// 
			this->pictureBox_after_image->BackColor = System::Drawing::SystemColors::ControlLightLight;
			this->pictureBox_after_image->Location = System::Drawing::Point(493, 46);
			this->pictureBox_after_image->Margin = System::Windows::Forms::Padding(2);
			this->pictureBox_after_image->Name = L"pictureBox_after_image";
			this->pictureBox_after_image->Size = System::Drawing::Size(450, 338);
			this->pictureBox_after_image->SizeMode = System::Windows::Forms::PictureBoxSizeMode::Zoom;
			this->pictureBox_after_image->TabIndex = 3;
			this->pictureBox_after_image->TabStop = false;
			this->pictureBox_after_image->Click += gcnew System::EventHandler(this, &MyForm::pictureBox_after_image_Click);
			// 
			// button_undo
			// 
			this->button_undo->Location = System::Drawing::Point(1123, 723);
			this->button_undo->Margin = System::Windows::Forms::Padding(2);
			this->button_undo->Name = L"button_undo";
			this->button_undo->Size = System::Drawing::Size(148, 42);
			this->button_undo->TabIndex = 4;
			this->button_undo->Text = L"Undo";
			this->button_undo->UseVisualStyleBackColor = true;
			this->button_undo->Click += gcnew System::EventHandler(this, &MyForm::button_undo_handler);
			// 
			// openImageWindow
			// 
			this->openImageWindow->FileName = L"openImageWindow";
			this->openImageWindow->Multiselect = true;
			// 
			// chart_before_histogram
			// 
			chartArea1->Name = L"ChartArea1";
			this->chart_before_histogram->ChartAreas->Add(chartArea1);
			legend1->Name = L"Legend1";
			this->chart_before_histogram->Legends->Add(legend1);
			this->chart_before_histogram->Location = System::Drawing::Point(19, 427);
			this->chart_before_histogram->Margin = System::Windows::Forms::Padding(2);
			this->chart_before_histogram->Name = L"chart_before_histogram";
			series1->ChartArea = L"ChartArea1";
			series1->IsVisibleInLegend = false;
			series1->Legend = L"Legend1";
			series1->Name = L"histogram";
			this->chart_before_histogram->Series->Add(series1);
			this->chart_before_histogram->Size = System::Drawing::Size(450, 338);
			this->chart_before_histogram->TabIndex = 5;
			// 
			// chart_after_histogram
			// 
			chartArea2->Name = L"ChartArea1";
			this->chart_after_histogram->ChartAreas->Add(chartArea2);
			legend2->Name = L"Legend1";
			this->chart_after_histogram->Legends->Add(legend2);
			this->chart_after_histogram->Location = System::Drawing::Point(493, 427);
			this->chart_after_histogram->Margin = System::Windows::Forms::Padding(2);
			this->chart_after_histogram->Name = L"chart_after_histogram";
			series2->ChartArea = L"ChartArea1";
			series2->IsVisibleInLegend = false;
			series2->Legend = L"Legend1";
			series2->Name = L"histogram";
			this->chart_after_histogram->Series->Add(series2);
			this->chart_after_histogram->Size = System::Drawing::Size(450, 338);
			this->chart_after_histogram->TabIndex = 6;
			// 
			// button_smooth_filter
			// 
			this->button_smooth_filter->Location = System::Drawing::Point(971, 164);
			this->button_smooth_filter->Margin = System::Windows::Forms::Padding(2);
			this->button_smooth_filter->Name = L"button_smooth_filter";
			this->button_smooth_filter->Size = System::Drawing::Size(299, 34);
			this->button_smooth_filter->TabIndex = 10;
			this->button_smooth_filter->Text = L"Smooth filter";
			this->button_smooth_filter->UseVisualStyleBackColor = true;
			this->button_smooth_filter->Click += gcnew System::EventHandler(this, &MyForm::button_smooth_filter_handler);
			// 
			// button_histogram_equalization
			// 
			this->button_histogram_equalization->Location = System::Drawing::Point(971, 258);
			this->button_histogram_equalization->Margin = System::Windows::Forms::Padding(2);
			this->button_histogram_equalization->Name = L"button_histogram_equalization";
			this->button_histogram_equalization->Size = System::Drawing::Size(299, 34);
			this->button_histogram_equalization->TabIndex = 14;
			this->button_histogram_equalization->Text = L"Histogram Equalization";
			this->button_histogram_equalization->UseVisualStyleBackColor = true;
			this->button_histogram_equalization->Click += gcnew System::EventHandler(this, &MyForm::button_histogram_equalization_handler);
			// 
			// button_defined_thresholding
			// 
			this->button_defined_thresholding->Location = System::Drawing::Point(971, 305);
			this->button_defined_thresholding->Margin = System::Windows::Forms::Padding(2);
			this->button_defined_thresholding->Name = L"button_defined_thresholding";
			this->button_defined_thresholding->Size = System::Drawing::Size(299, 34);
			this->button_defined_thresholding->TabIndex = 15;
			this->button_defined_thresholding->Text = L"Defined Thresholding";
			this->button_defined_thresholding->UseVisualStyleBackColor = true;
			this->button_defined_thresholding->Click += gcnew System::EventHandler(this, &MyForm::button_defined_thresholding_handler);
			// 
			// button_sobel_edge_detection
			// 
			this->button_sobel_edge_detection->Location = System::Drawing::Point(971, 393);
			this->button_sobel_edge_detection->Margin = System::Windows::Forms::Padding(2);
			this->button_sobel_edge_detection->Name = L"button_sobel_edge_detection";
			this->button_sobel_edge_detection->Size = System::Drawing::Size(299, 34);
			this->button_sobel_edge_detection->TabIndex = 16;
			this->button_sobel_edge_detection->Text = L"Sobel Edge Detection";
			this->button_sobel_edge_detection->UseVisualStyleBackColor = true;
			this->button_sobel_edge_detection->Click += gcnew System::EventHandler(this, &MyForm::button_sobel_edge_detection_handler);
			// 
			// button_sobel_threshold_combined
			// 
			this->button_sobel_threshold_combined->Location = System::Drawing::Point(971, 485);
			this->button_sobel_threshold_combined->Margin = System::Windows::Forms::Padding(2);
			this->button_sobel_threshold_combined->Name = L"button_sobel_threshold_combined";
			this->button_sobel_threshold_combined->Size = System::Drawing::Size(299, 34);
			this->button_sobel_threshold_combined->TabIndex = 20;
			this->button_sobel_threshold_combined->Text = L"Sobel Threshold Combined";
			this->button_sobel_threshold_combined->UseVisualStyleBackColor = true;
			this->button_sobel_threshold_combined->Click += gcnew System::EventHandler(this, &MyForm::button_sobel_threshold_combined_handler);
			// 
			// button_connected_component
			// 
			this->button_connected_component->Location = System::Drawing::Point(971, 533);
			this->button_connected_component->Margin = System::Windows::Forms::Padding(2);
			this->button_connected_component->Name = L"button_connected_component";
			this->button_connected_component->Size = System::Drawing::Size(299, 34);
			this->button_connected_component->TabIndex = 21;
			this->button_connected_component->Text = L"Connected Component";
			this->button_connected_component->UseVisualStyleBackColor = true;
			this->button_connected_component->Click += gcnew System::EventHandler(this, &MyForm::button_connected_component_handler);
			// 
			// button_image_registration
			// 
			this->button_image_registration->Location = System::Drawing::Point(971, 627);
			this->button_image_registration->Margin = System::Windows::Forms::Padding(2);
			this->button_image_registration->Name = L"button_image_registration";
			this->button_image_registration->Size = System::Drawing::Size(299, 34);
			this->button_image_registration->TabIndex = 22;
			this->button_image_registration->Text = L"Image Registration";
			this->button_image_registration->UseVisualStyleBackColor = true;
			this->button_image_registration->Click += gcnew System::EventHandler(this, &MyForm::button_image_registration_handler);
			// 
			// label_scaling
			// 
			this->label_scaling->AutoSize = true;
			this->label_scaling->Location = System::Drawing::Point(4, 23);
			this->label_scaling->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_scaling->Name = L"label_scaling";
			this->label_scaling->Size = System::Drawing::Size(56, 12);
			this->label_scaling->TabIndex = 23;
			this->label_scaling->Text = L"Scaling = \?";
			// 
			// label_theta
			// 
			this->label_theta->AutoSize = true;
			this->label_theta->Location = System::Drawing::Point(84, 23);
			this->label_theta->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_theta->Name = L"label_theta";
			this->label_theta->Size = System::Drawing::Size(72, 12);
			this->label_theta->TabIndex = 24;
			this->label_theta->Text = L"        Theta = \?";
			// 
			// label_difference
			// 
			this->label_difference->AutoSize = true;
			this->label_difference->Location = System::Drawing::Point(201, 23);
			this->label_difference->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_difference->Name = L"label_difference";
			this->label_difference->Size = System::Drawing::Size(71, 12);
			this->label_difference->TabIndex = 25;
			this->label_difference->Text = L"Difference = \?";
			// 
			// label_before_image
			// 
			this->label_before_image->AutoSize = true;
			this->label_before_image->Location = System::Drawing::Point(195, 25);
			this->label_before_image->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_before_image->Name = L"label_before_image";
			this->label_before_image->Size = System::Drawing::Size(69, 12);
			this->label_before_image->TabIndex = 26;
			this->label_before_image->Text = L"Before Image";
			// 
			// label_after_image
			// 
			this->label_after_image->AutoSize = true;
			this->label_after_image->Location = System::Drawing::Point(691, 25);
			this->label_after_image->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_after_image->Name = L"label_after_image";
			this->label_after_image->Size = System::Drawing::Size(61, 12);
			this->label_after_image->TabIndex = 27;
			this->label_after_image->Text = L"After Image";
			// 
			// label_before_histogram
			// 
			this->label_before_histogram->AutoSize = true;
			this->label_before_histogram->Location = System::Drawing::Point(185, 404);
			this->label_before_histogram->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_before_histogram->Name = L"label_before_histogram";
			this->label_before_histogram->Size = System::Drawing::Size(88, 12);
			this->label_before_histogram->TabIndex = 28;
			this->label_before_histogram->Text = L"Before Histogram";
			// 
			// label_after_histogram
			// 
			this->label_after_histogram->AutoSize = true;
			this->label_after_histogram->Location = System::Drawing::Point(680, 404);
			this->label_after_histogram->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_after_histogram->Name = L"label_after_histogram";
			this->label_after_histogram->Size = System::Drawing::Size(80, 12);
			this->label_after_histogram->TabIndex = 29;
			this->label_after_histogram->Text = L"After Histogram";
			// 
			// radioButton_r_channel
			// 
			this->radioButton_r_channel->AutoSize = true;
			this->radioButton_r_channel->Location = System::Drawing::Point(8, 19);
			this->radioButton_r_channel->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_r_channel->Name = L"radioButton_r_channel";
			this->radioButton_r_channel->Size = System::Drawing::Size(73, 16);
			this->radioButton_r_channel->TabIndex = 30;
			this->radioButton_r_channel->TabStop = true;
			this->radioButton_r_channel->Text = L"R Channel";
			this->radioButton_r_channel->UseVisualStyleBackColor = true;
			// 
			// radioButton_g_channel
			// 
			this->radioButton_g_channel->AutoSize = true;
			this->radioButton_g_channel->Location = System::Drawing::Point(101, 19);
			this->radioButton_g_channel->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_g_channel->Name = L"radioButton_g_channel";
			this->radioButton_g_channel->Size = System::Drawing::Size(73, 16);
			this->radioButton_g_channel->TabIndex = 31;
			this->radioButton_g_channel->TabStop = true;
			this->radioButton_g_channel->Text = L"G Channel";
			this->radioButton_g_channel->UseVisualStyleBackColor = true;
			// 
			// groupBox_rgb_extraction
			// 
			this->groupBox_rgb_extraction->Controls->Add(this->radioButton_r_channel);
			this->groupBox_rgb_extraction->Controls->Add(this->radioButton_grayscale);
			this->groupBox_rgb_extraction->Controls->Add(this->radioButton_g_channel);
			this->groupBox_rgb_extraction->Controls->Add(this->radioButton_b_channel);
			this->groupBox_rgb_extraction->Location = System::Drawing::Point(971, 82);
			this->groupBox_rgb_extraction->Margin = System::Windows::Forms::Padding(2);
			this->groupBox_rgb_extraction->Name = L"groupBox_rgb_extraction";
			this->groupBox_rgb_extraction->Padding = System::Windows::Forms::Padding(2);
			this->groupBox_rgb_extraction->Size = System::Drawing::Size(299, 73);
			this->groupBox_rgb_extraction->TabIndex = 32;
			this->groupBox_rgb_extraction->TabStop = false;
			// 
			// radioButton_grayscale
			// 
			this->radioButton_grayscale->AutoSize = true;
			this->radioButton_grayscale->Location = System::Drawing::Point(101, 39);
			this->radioButton_grayscale->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_grayscale->Name = L"radioButton_grayscale";
			this->radioButton_grayscale->Size = System::Drawing::Size(68, 16);
			this->radioButton_grayscale->TabIndex = 34;
			this->radioButton_grayscale->TabStop = true;
			this->radioButton_grayscale->Text = L"Grayscale";
			this->radioButton_grayscale->UseVisualStyleBackColor = true;
			// 
			// radioButton_b_channel
			// 
			this->radioButton_b_channel->AutoSize = true;
			this->radioButton_b_channel->Location = System::Drawing::Point(8, 39);
			this->radioButton_b_channel->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_b_channel->Name = L"radioButton_b_channel";
			this->radioButton_b_channel->Size = System::Drawing::Size(73, 16);
			this->radioButton_b_channel->TabIndex = 33;
			this->radioButton_b_channel->TabStop = true;
			this->radioButton_b_channel->Text = L"B Channel";
			this->radioButton_b_channel->UseVisualStyleBackColor = true;
			// 
			// groupBox_smooth_filter
			// 
			this->groupBox_smooth_filter->Controls->Add(this->radioButton_mean);
			this->groupBox_smooth_filter->Controls->Add(this->radioButton_median);
			this->groupBox_smooth_filter->Location = System::Drawing::Point(971, 200);
			this->groupBox_smooth_filter->Margin = System::Windows::Forms::Padding(2);
			this->groupBox_smooth_filter->Name = L"groupBox_smooth_filter";
			this->groupBox_smooth_filter->Padding = System::Windows::Forms::Padding(2);
			this->groupBox_smooth_filter->Size = System::Drawing::Size(299, 47);
			this->groupBox_smooth_filter->TabIndex = 35;
			this->groupBox_smooth_filter->TabStop = false;
			// 
			// radioButton_mean
			// 
			this->radioButton_mean->AutoSize = true;
			this->radioButton_mean->Location = System::Drawing::Point(8, 19);
			this->radioButton_mean->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_mean->Name = L"radioButton_mean";
			this->radioButton_mean->Size = System::Drawing::Size(49, 16);
			this->radioButton_mean->TabIndex = 30;
			this->radioButton_mean->TabStop = true;
			this->radioButton_mean->Text = L"Mean";
			this->radioButton_mean->UseVisualStyleBackColor = true;
			// 
			// radioButton_median
			// 
			this->radioButton_median->AutoSize = true;
			this->radioButton_median->Location = System::Drawing::Point(101, 19);
			this->radioButton_median->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_median->Name = L"radioButton_median";
			this->radioButton_median->Size = System::Drawing::Size(58, 16);
			this->radioButton_median->TabIndex = 30;
			this->radioButton_median->TabStop = true;
			this->radioButton_median->Text = L"Median";
			this->radioButton_median->UseVisualStyleBackColor = true;
			// 
			// radioButton_vertical
			// 
			this->radioButton_vertical->AutoSize = true;
			this->radioButton_vertical->Location = System::Drawing::Point(8, 19);
			this->radioButton_vertical->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_vertical->Name = L"radioButton_vertical";
			this->radioButton_vertical->Size = System::Drawing::Size(59, 16);
			this->radioButton_vertical->TabIndex = 34;
			this->radioButton_vertical->TabStop = true;
			this->radioButton_vertical->Text = L"Vertical";
			this->radioButton_vertical->UseVisualStyleBackColor = true;
			// 
			// groupBox_sobel_edge_detection
			// 
			this->groupBox_sobel_edge_detection->Controls->Add(this->radioButton_combined);
			this->groupBox_sobel_edge_detection->Controls->Add(this->radioButton_horizontal);
			this->groupBox_sobel_edge_detection->Controls->Add(this->radioButton_vertical);
			this->groupBox_sobel_edge_detection->Location = System::Drawing::Point(971, 429);
			this->groupBox_sobel_edge_detection->Margin = System::Windows::Forms::Padding(2);
			this->groupBox_sobel_edge_detection->Name = L"groupBox_sobel_edge_detection";
			this->groupBox_sobel_edge_detection->Padding = System::Windows::Forms::Padding(2);
			this->groupBox_sobel_edge_detection->Size = System::Drawing::Size(299, 47);
			this->groupBox_sobel_edge_detection->TabIndex = 36;
			this->groupBox_sobel_edge_detection->TabStop = false;
			// 
			// radioButton_combined
			// 
			this->radioButton_combined->AutoSize = true;
			this->radioButton_combined->Location = System::Drawing::Point(184, 19);
			this->radioButton_combined->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_combined->Name = L"radioButton_combined";
			this->radioButton_combined->Size = System::Drawing::Size(72, 16);
			this->radioButton_combined->TabIndex = 35;
			this->radioButton_combined->TabStop = true;
			this->radioButton_combined->Text = L"Combined";
			this->radioButton_combined->UseVisualStyleBackColor = true;
			// 
			// radioButton_horizontal
			// 
			this->radioButton_horizontal->AutoSize = true;
			this->radioButton_horizontal->Location = System::Drawing::Point(96, 19);
			this->radioButton_horizontal->Margin = System::Windows::Forms::Padding(2);
			this->radioButton_horizontal->Name = L"radioButton_horizontal";
			this->radioButton_horizontal->Size = System::Drawing::Size(72, 16);
			this->radioButton_horizontal->TabIndex = 34;
			this->radioButton_horizontal->TabStop = true;
			this->radioButton_horizontal->Text = L"Horizontal";
			this->radioButton_horizontal->UseVisualStyleBackColor = true;
			// 
			// trackBar_defined_thresholding
			// 
			this->trackBar_defined_thresholding->Location = System::Drawing::Point(971, 348);
			this->trackBar_defined_thresholding->Margin = System::Windows::Forms::Padding(2);
			this->trackBar_defined_thresholding->Maximum = 255;
			this->trackBar_defined_thresholding->Name = L"trackBar_defined_thresholding";
			this->trackBar_defined_thresholding->Size = System::Drawing::Size(299, 45);
			this->trackBar_defined_thresholding->TabIndex = 38;
			this->trackBar_defined_thresholding->Value = 200;
			// 
			// label_control
			// 
			this->label_control->AutoSize = true;
			this->label_control->Location = System::Drawing::Point(1097, 25);
			this->label_control->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_control->Name = L"label_control";
			this->label_control->Size = System::Drawing::Size(41, 12);
			this->label_control->TabIndex = 39;
			this->label_control->Text = L"Control";
			// 
			// groupBox_image_registration
			// 
			this->groupBox_image_registration->Controls->Add(this->label_scaling);
			this->groupBox_image_registration->Controls->Add(this->label_theta);
			this->groupBox_image_registration->Controls->Add(this->label_difference);
			this->groupBox_image_registration->Location = System::Drawing::Point(971, 666);
			this->groupBox_image_registration->Margin = System::Windows::Forms::Padding(2);
			this->groupBox_image_registration->Name = L"groupBox_image_registration";
			this->groupBox_image_registration->Padding = System::Windows::Forms::Padding(2);
			this->groupBox_image_registration->Size = System::Drawing::Size(299, 47);
			this->groupBox_image_registration->TabIndex = 40;
			this->groupBox_image_registration->TabStop = false;
			// 
			// groupBox_connected_component
			// 
			this->groupBox_connected_component->Controls->Add(this->label_connected_component);
			this->groupBox_connected_component->Location = System::Drawing::Point(971, 570);
			this->groupBox_connected_component->Margin = System::Windows::Forms::Padding(2);
			this->groupBox_connected_component->Name = L"groupBox_connected_component";
			this->groupBox_connected_component->Padding = System::Windows::Forms::Padding(2);
			this->groupBox_connected_component->Size = System::Drawing::Size(299, 47);
			this->groupBox_connected_component->TabIndex = 41;
			this->groupBox_connected_component->TabStop = false;
			// 
			// label_connected_component
			// 
			this->label_connected_component->AutoSize = true;
			this->label_connected_component->Location = System::Drawing::Point(5, 19);
			this->label_connected_component->Margin = System::Windows::Forms::Padding(2, 0, 2, 0);
			this->label_connected_component->Name = L"label_connected_component";
			this->label_connected_component->Size = System::Drawing::Size(184, 12);
			this->label_connected_component->TabIndex = 23;
			this->label_connected_component->Text = L"Number of Connected Component = \?";
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(6, 12);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(1295, 785);
			this->Controls->Add(this->groupBox_connected_component);
			this->Controls->Add(this->groupBox_image_registration);
			this->Controls->Add(this->label_control);
			this->Controls->Add(this->trackBar_defined_thresholding);
			this->Controls->Add(this->groupBox_sobel_edge_detection);
			this->Controls->Add(this->groupBox_smooth_filter);
			this->Controls->Add(this->button_defined_thresholding);
			this->Controls->Add(this->groupBox_rgb_extraction);
			this->Controls->Add(this->label_after_histogram);
			this->Controls->Add(this->label_before_histogram);
			this->Controls->Add(this->label_after_image);
			this->Controls->Add(this->label_before_image);
			this->Controls->Add(this->button_image_registration);
			this->Controls->Add(this->button_connected_component);
			this->Controls->Add(this->button_sobel_threshold_combined);
			this->Controls->Add(this->button_sobel_edge_detection);
			this->Controls->Add(this->button_histogram_equalization);
			this->Controls->Add(this->button_smooth_filter);
			this->Controls->Add(this->chart_after_histogram);
			this->Controls->Add(this->chart_before_histogram);
			this->Controls->Add(this->button_undo);
			this->Controls->Add(this->pictureBox_after_image);
			this->Controls->Add(this->pictureBox_before_image);
			this->Controls->Add(this->button_rgb_extraction);
			this->Controls->Add(this->button_load);
			this->Margin = System::Windows::Forms::Padding(2);
			this->Name = L"MyForm";
			this->Text = L"Image Processing System";
			this->Load += gcnew System::EventHandler(this, &MyForm::MyForm_Load);
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox_before_image))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox_after_image))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart_before_histogram))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->chart_after_histogram))->EndInit();
			this->groupBox_rgb_extraction->ResumeLayout(false);
			this->groupBox_rgb_extraction->PerformLayout();
			this->groupBox_smooth_filter->ResumeLayout(false);
			this->groupBox_smooth_filter->PerformLayout();
			this->groupBox_sobel_edge_detection->ResumeLayout(false);
			this->groupBox_sobel_edge_detection->PerformLayout();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->trackBar_defined_thresholding))->EndInit();
			this->groupBox_image_registration->ResumeLayout(false);
			this->groupBox_image_registration->PerformLayout();
			this->groupBox_connected_component->ResumeLayout(false);
			this->groupBox_connected_component->PerformLayout();
			this->ResumeLayout(false);
			this->PerformLayout();

		}
#pragma endregion
	private: Bitmap^ originImage;
	private: Bitmap^ transferImage;
	private: int* originPos = new int[4];
	private: int* transferPos = new int[4];
	private: int countOriginPoints;
	private: int countTransferPoints;

	/* ==================================== Functional Button ==================================== */

	private: System::Void MyForm_Load(System::Object^  sender, System::EventArgs^  e) {
		originImage = nullptr;
		transferImage = nullptr;
	}

	private: System::Void button_load_handler(System::Object^  sender, System::EventArgs^  e) {

		int countFiles = 0;
		string files[2];

		if (openImageWindow->ShowDialog() == System::Windows::Forms::DialogResult::OK) {

			saveResult();
			removeAllChart();
			resetPictureBoxPoint();

			for each(String^ file in openImageWindow->FileNames) {
				files[countFiles] = stringTransfer(file);
				countFiles += 1;
			}

			if (countFiles == 2) {
				originImage = gcnew Bitmap(stringTransfer(files[1]));
				transferImage = gcnew Bitmap(stringTransfer(files[0]));
			} else {
				originImage = gcnew Bitmap(stringTransfer(files[0]));
				transferImage = nullptr;

			}

			setPictureBox(pictureBox_before_image, originImage);
			setPictureBox(pictureBox_after_image, transferImage);

		}
	}

	private: System::Void button_undo_handler(System::Object^  sender, System::EventArgs^  e) {

		if (imageCache.size() <= 0) {
			return;
		}

		vector <vector<vector<vector<int>>> > previousImage = imageCache.back();
		vector < map<int, int> > previousChart = chartCache.back();

		imageCache.pop_back();
		chartCache.pop_back();

		if (previousImage.size() == 0) {
			originImage = nullptr;
			transferImage = nullptr;

		} else if (previousImage.size() == 1) {
			originImage = bitmapVectorTransfer(previousImage.front());
			transferImage = nullptr;

		} else {
			originImage = bitmapVectorTransfer(previousImage.front());
			transferImage = bitmapVectorTransfer(previousImage.back());
		}

		originImageCollection = previousChart.front();
		transferImageCollection = previousChart.back();

		setPictureBox(pictureBox_before_image, originImage);
		setPictureBox(pictureBox_after_image, transferImage);

		setChart(chart_before_histogram, originImageCollection);
		setChart(chart_after_histogram, transferImageCollection);
	}

	private: void saveResult() {
		vector< vector<vector<vector<int>>> > currentImage;
		vector < map<int, int> > currentChart;

		if (isExist(originImage)) {
			currentImage.push_back(bitmapVectorTransfer(originImage));
		}

		if (isExist(transferImage)) {
			currentImage.push_back(bitmapVectorTransfer(transferImage));
		}

		currentChart.push_back(originImageCollection);
		currentChart.push_back(transferImageCollection);

		imageCache.push_back(currentImage);
		chartCache.push_back(currentChart);

	}

	private: void setPictureBox(PictureBox^ %pictureBox, Bitmap^ image) {
		pictureBox->Image = image;
	}

	private: void setLabel(Label^ %label, String^ str) {
		label->Text = str;
	}

	private: void setChart(Chart^ %chart, map<int, int> imageCollection) {
		String^ key = "histogram";
		bool isEmpty = true;
		for (int intGray = 0; intGray < 256; intGray++) {
			if (imageCollection.find(intGray) != imageCollection.end()) {
				chart->Series[key]->Points->AddXY(intGray, imageCollection[intGray]);
				isEmpty = false;
			}
		}
		if (isEmpty) {
			removeAllChart();
		}
	}

	private: void removeAllChart() {
		String^ key = "histogram";
		map<int, int> empty;
		originImageCollection = empty;
		transferImageCollection = empty;
		chart_before_histogram->Series[key]->Points->Clear();
		chart_after_histogram->Series[key]->Points->Clear();
	}

	private: void resetPictureBoxPoint() {
		originPos = new int[4];
		transferPos = new int[4];
		countOriginPoints = 0;
		countTransferPoints = 0;
	}

	private: vector<int> zoomPointTranslate(int pos[2], Bitmap^ image, PictureBox^ pictureBox) {
		vector<int> translatePos;
		double scale = max((double)(image->Width) / (double)(pictureBox->Width), (double)(image->Height) / (double)(pictureBox->Height));
		double translate[2] = { 
			abs(pictureBox->Width * scale - image->Width) / 2,
			abs(pictureBox->Height * scale - image->Height) / 2
		};
		translatePos.push_back((int)(scale * pos[0] - translate[0]));
		translatePos.push_back((int)(scale * pos[1] - translate[1]));

		return translatePos;
	}

	private: void swapImage() {
		saveResult();

		Bitmap^ tempImage;
		tempImage = originImage;
		originImage = transferImage;
		transferImage = tempImage;

		int* tempPos = new int[4];
		tempPos = originPos;
		originPos = transferPos;
		transferPos = tempPos;

		int countTempPoints;
		countTempPoints = countOriginPoints;
		countOriginPoints = countTransferPoints;
		countTransferPoints = countTempPoints;

		setPictureBox(pictureBox_before_image, originImage);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: bool isExist(Bitmap^ image) {
		return image != nullptr;
	}

	/* ==================================== Filter Method Button ==================================== */

	private: System::Void button_rgb_extraction_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		char kind;

		if (radioButton_r_channel->Checked) {
			kind = 'r';
		} else if (radioButton_g_channel->Checked) {
			kind = 'g';
		} else if (radioButton_b_channel->Checked) {
			kind = 'b';
		} else if (radioButton_grayscale->Checked) {
			kind = '.';
		} else {
			return;
		}

		transferImage = rgb_extraction_transformation(originImage, kind);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_smooth_filter_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		char kind;

		if (radioButton_mean->Checked) {
			kind = 'a';
		} else if (radioButton_median->Checked) {
			kind = 'm';
		} else {
			return;
		}

		transferImage = smooth_filter(originImage, kind);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_histogram_equalization_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		transferImage = histogram_equalization(originImage);
		setPictureBox(pictureBox_after_image, transferImage);
		setChart(chart_before_histogram, originImageCollection);
		setChart(chart_after_histogram, transferImageCollection);
	}

	private: System::Void button_defined_thresholding_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		int threshold = trackBar_defined_thresholding->Value;

		transferImage = define_thresholding(originImage, threshold);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_sobel_edge_detection_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		char kind;

		if (radioButton_horizontal->Checked) {
			kind = 'h';
		} else if (radioButton_vertical->Checked) {
			kind = 'v';
		} else if (radioButton_combined->Checked) {
			kind = 'c';
		} else {
			return;
		}

		transferImage = sobel_edge_dection(originImage, kind);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_sobel_threshold_combined_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		int threshold = trackBar_defined_thresholding->Value;

		transferImage = sobel_threshold_combine(originImage, threshold);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_connected_component_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		saveResult();
		removeAllChart();

		transferImage = connected_component(originImage);
		setLabel(label_connected_component, "Number of Connected Component = " + count_region);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_image_registration_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false || isExist(transferImage) == false) {
			return;
		}

		if (countOriginPoints != 4 || countTransferPoints != 4) {
			return;
		}

		saveResult();
		removeAllChart();

		transferImage = image_registration(originImage, transferImage, originPos, transferPos);
		setPictureBox(pictureBox_after_image, transferImage);
		setLabel(label_scaling, "Scaling = " + round(100 * scale) / 100);
		setLabel(label_theta, "Theta = " + round(100 * angle * 180 / 3.14159) / 100 + " (degree)");
		setLabel(label_difference, "Difference = " + round(100 * difference) / 100);
	}

	private: System::Void pictureBox_before_image_Click(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false || isExist(transferImage) == false) {
			return;
		}

		MouseEventArgs ^event = (MouseEventArgs^)e;
		if (event->Button == System::Windows::Forms::MouseButtons::Right) {
			swapImage();
			return;
		}

		if (countOriginPoints == 4) {
			originPos = new int[4];
			countOriginPoints = 0;
		}

		// Not already to support (countOriginPoints should reset)
		// saveResult();

		Graphics^ before_image_graph = Graphics::FromImage(pictureBox_before_image->Image);
		Point LocalMousePosition = pictureBox_before_image->PointToClient(Cursor->Position);
		int position[2] = { LocalMousePosition.X , LocalMousePosition.Y };
		vector<int> translatePos = zoomPointTranslate(position, originImage, pictureBox_before_image);
		translatePos[0] -= 8;
		translatePos[1] -= 8;

		if (translatePos[0] < 0 || translatePos[1] < 0) {
			return;
		}

		before_image_graph->FillEllipse(Brushes::Red, translatePos[0], translatePos[1], 16, 16);

		setPictureBox(pictureBox_before_image, originImage);
		// cout << translatePos[0] << ":" << translatePos[1] << endl;

		originPos[countOriginPoints++] = translatePos[0];
		originPos[countOriginPoints++] = translatePos[1];
	}

	private: System::Void pictureBox_after_image_Click(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false || isExist(transferImage) == false) {
			return;
		}

		MouseEventArgs ^event = (MouseEventArgs^) e;
		if (event->Button == System::Windows::Forms::MouseButtons::Right) {
			swapImage();
			return;
		}

		if (countTransferPoints == 4) {
			transferPos = new int[4];
			countTransferPoints = 0;
		}

		// Not already to support (countTransferPoints should reset)
		// saveResult();

		Graphics^ after_image_graph = Graphics::FromImage(pictureBox_after_image->Image);
		Point LocalMousePosition = pictureBox_after_image->PointToClient(Cursor->Position);
		int position[2] = { LocalMousePosition.X , LocalMousePosition.Y };
		vector<int> translatePos = zoomPointTranslate(position, transferImage, pictureBox_after_image);
		translatePos[0] -= 8;
		translatePos[1] -= 8;

		if (translatePos[0] < 0 || translatePos[1] < 0) {
			return;
		}

		after_image_graph->FillEllipse(Brushes::Red, translatePos[0], translatePos[1], 16, 16);

		setPictureBox(pictureBox_after_image, transferImage);
		// cout << translatePos[0] << ":" << translatePos[1] << endl;

		transferPos[countTransferPoints++] = translatePos[0];
		transferPos[countTransferPoints++] = translatePos[1];
	}

};
}

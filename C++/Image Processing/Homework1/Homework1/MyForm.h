#include "Function.h"
#include "Smooth_Filter.h"
#include "Connected_Component.h"
#include "Define_Thresholding.h"
#include "Sobel_Edge_Detection.h"
#include "Sobel_Threshold_Combine.h"
#include "RGB_Extraction_Transformation.h"

#include <iostream>
#include <string>
#include <vector>

namespace Homework1 {

	using namespace std;
	using namespace System;
	using namespace System::ComponentModel;
	using namespace System::Collections;
	using namespace System::Windows::Forms;
	using namespace System::Data;
	using namespace System::Drawing;

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
			System::Windows::Forms::DataVisualization::Charting::ChartArea^  chartArea5 = (gcnew System::Windows::Forms::DataVisualization::Charting::ChartArea());
			System::Windows::Forms::DataVisualization::Charting::Legend^  legend5 = (gcnew System::Windows::Forms::DataVisualization::Charting::Legend());
			System::Windows::Forms::DataVisualization::Charting::Series^  series5 = (gcnew System::Windows::Forms::DataVisualization::Charting::Series());
			System::Windows::Forms::DataVisualization::Charting::ChartArea^  chartArea6 = (gcnew System::Windows::Forms::DataVisualization::Charting::ChartArea());
			System::Windows::Forms::DataVisualization::Charting::Legend^  legend6 = (gcnew System::Windows::Forms::DataVisualization::Charting::Legend());
			System::Windows::Forms::DataVisualization::Charting::Series^  series6 = (gcnew System::Windows::Forms::DataVisualization::Charting::Series());
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
			this->button_load->Location = System::Drawing::Point(1295, 904);
			this->button_load->Name = L"button_load";
			this->button_load->Size = System::Drawing::Size(197, 52);
			this->button_load->TabIndex = 0;
			this->button_load->Text = L"Load";
			this->button_load->UseVisualStyleBackColor = true;
			this->button_load->Click += gcnew System::EventHandler(this, &MyForm::button_load_handler);
			// 
			// button_rgb_extraction
			// 
			this->button_rgb_extraction->Location = System::Drawing::Point(1295, 58);
			this->button_rgb_extraction->Name = L"button_rgb_extraction";
			this->button_rgb_extraction->Size = System::Drawing::Size(399, 43);
			this->button_rgb_extraction->TabIndex = 1;
			this->button_rgb_extraction->Text = L"RGB Extraction";
			this->button_rgb_extraction->UseVisualStyleBackColor = true;
			this->button_rgb_extraction->Click += gcnew System::EventHandler(this, &MyForm::button_rgb_extraction_handler);
			// 
			// pictureBox_before_image
			// 
			this->pictureBox_before_image->BackColor = System::Drawing::SystemColors::ControlLightLight;
			this->pictureBox_before_image->Location = System::Drawing::Point(25, 58);
			this->pictureBox_before_image->Name = L"pictureBox_before_image";
			this->pictureBox_before_image->Size = System::Drawing::Size(600, 422);
			this->pictureBox_before_image->SizeMode = System::Windows::Forms::PictureBoxSizeMode::Zoom;
			this->pictureBox_before_image->TabIndex = 2;
			this->pictureBox_before_image->TabStop = false;
			// 
			// pictureBox_after_image
			// 
			this->pictureBox_after_image->BackColor = System::Drawing::SystemColors::ControlLightLight;
			this->pictureBox_after_image->Location = System::Drawing::Point(657, 58);
			this->pictureBox_after_image->Name = L"pictureBox_after_image";
			this->pictureBox_after_image->Size = System::Drawing::Size(600, 422);
			this->pictureBox_after_image->SizeMode = System::Windows::Forms::PictureBoxSizeMode::Zoom;
			this->pictureBox_after_image->TabIndex = 3;
			this->pictureBox_after_image->TabStop = false;
			// 
			// button_undo
			// 
			this->button_undo->Location = System::Drawing::Point(1497, 904);
			this->button_undo->Name = L"button_undo";
			this->button_undo->Size = System::Drawing::Size(197, 52);
			this->button_undo->TabIndex = 4;
			this->button_undo->Text = L"Undo";
			this->button_undo->UseVisualStyleBackColor = true;
			this->button_undo->Click += gcnew System::EventHandler(this, &MyForm::button_undo_handler);
			// 
			// openImageWindow
			// 
			this->openImageWindow->FileName = L"openImageWindow";
			// 
			// chart_before_histogram
			// 
			chartArea5->Name = L"ChartArea1";
			this->chart_before_histogram->ChartAreas->Add(chartArea5);
			legend5->Name = L"Legend1";
			this->chart_before_histogram->Legends->Add(legend5);
			this->chart_before_histogram->Location = System::Drawing::Point(25, 534);
			this->chart_before_histogram->Name = L"chart_before_histogram";
			series5->ChartArea = L"ChartArea1";
			series5->Legend = L"Legend1";
			series5->Name = L"Series1";
			this->chart_before_histogram->Series->Add(series5);
			this->chart_before_histogram->Size = System::Drawing::Size(600, 422);
			this->chart_before_histogram->TabIndex = 5;
			// 
			// chart_after_histogram
			// 
			chartArea6->Name = L"ChartArea1";
			this->chart_after_histogram->ChartAreas->Add(chartArea6);
			legend6->Name = L"Legend1";
			this->chart_after_histogram->Legends->Add(legend6);
			this->chart_after_histogram->Location = System::Drawing::Point(657, 534);
			this->chart_after_histogram->Name = L"chart_after_histogram";
			series6->ChartArea = L"ChartArea1";
			series6->Legend = L"Legend1";
			series6->Name = L"Series1";
			this->chart_after_histogram->Series->Add(series6);
			this->chart_after_histogram->Size = System::Drawing::Size(600, 422);
			this->chart_after_histogram->TabIndex = 6;
			// 
			// button_smooth_filter
			// 
			this->button_smooth_filter->Location = System::Drawing::Point(1295, 205);
			this->button_smooth_filter->Name = L"button_smooth_filter";
			this->button_smooth_filter->Size = System::Drawing::Size(399, 43);
			this->button_smooth_filter->TabIndex = 10;
			this->button_smooth_filter->Text = L"Smooth filter";
			this->button_smooth_filter->UseVisualStyleBackColor = true;
			this->button_smooth_filter->Click += gcnew System::EventHandler(this, &MyForm::button_smooth_filter_handler);
			// 
			// button_histogram_equalization
			// 
			this->button_histogram_equalization->Location = System::Drawing::Point(1295, 323);
			this->button_histogram_equalization->Name = L"button_histogram_equalization";
			this->button_histogram_equalization->Size = System::Drawing::Size(399, 43);
			this->button_histogram_equalization->TabIndex = 14;
			this->button_histogram_equalization->Text = L"Histogram Equalization";
			this->button_histogram_equalization->UseVisualStyleBackColor = true;
			this->button_histogram_equalization->Click += gcnew System::EventHandler(this, &MyForm::button_histogram_equalization_handler);
			// 
			// button_defined_thresholding
			// 
			this->button_defined_thresholding->Location = System::Drawing::Point(1295, 381);
			this->button_defined_thresholding->Name = L"button_defined_thresholding";
			this->button_defined_thresholding->Size = System::Drawing::Size(399, 43);
			this->button_defined_thresholding->TabIndex = 15;
			this->button_defined_thresholding->Text = L"Defined Thresholding";
			this->button_defined_thresholding->UseVisualStyleBackColor = true;
			this->button_defined_thresholding->Click += gcnew System::EventHandler(this, &MyForm::button_defined_thresholding_handler);
			// 
			// button_sobel_edge_detection
			// 
			this->button_sobel_edge_detection->Location = System::Drawing::Point(1295, 491);
			this->button_sobel_edge_detection->Name = L"button_sobel_edge_detection";
			this->button_sobel_edge_detection->Size = System::Drawing::Size(399, 43);
			this->button_sobel_edge_detection->TabIndex = 16;
			this->button_sobel_edge_detection->Text = L"Sobel Edge Detection";
			this->button_sobel_edge_detection->UseVisualStyleBackColor = true;
			this->button_sobel_edge_detection->Click += gcnew System::EventHandler(this, &MyForm::button_sobel_edge_detection_handler);
			// 
			// button_sobel_threshold_combined
			// 
			this->button_sobel_threshold_combined->Location = System::Drawing::Point(1295, 606);
			this->button_sobel_threshold_combined->Name = L"button_sobel_threshold_combined";
			this->button_sobel_threshold_combined->Size = System::Drawing::Size(399, 43);
			this->button_sobel_threshold_combined->TabIndex = 20;
			this->button_sobel_threshold_combined->Text = L"Sobel Threshold Combined";
			this->button_sobel_threshold_combined->UseVisualStyleBackColor = true;
			this->button_sobel_threshold_combined->Click += gcnew System::EventHandler(this, &MyForm::button_sobel_threshold_combined_handler);
			// 
			// button_connected_component
			// 
			this->button_connected_component->Location = System::Drawing::Point(1295, 666);
			this->button_connected_component->Name = L"button_connected_component";
			this->button_connected_component->Size = System::Drawing::Size(399, 43);
			this->button_connected_component->TabIndex = 21;
			this->button_connected_component->Text = L"Connected Component";
			this->button_connected_component->UseVisualStyleBackColor = true;
			this->button_connected_component->Click += gcnew System::EventHandler(this, &MyForm::button_connected_component_handler);
			// 
			// button_image_registration
			// 
			this->button_image_registration->Location = System::Drawing::Point(1295, 784);
			this->button_image_registration->Name = L"button_image_registration";
			this->button_image_registration->Size = System::Drawing::Size(399, 43);
			this->button_image_registration->TabIndex = 22;
			this->button_image_registration->Text = L"Image Registration";
			this->button_image_registration->UseVisualStyleBackColor = true;
			this->button_image_registration->Click += gcnew System::EventHandler(this, &MyForm::button_image_registration_handler);
			// 
			// label_scaling
			// 
			this->label_scaling->AutoSize = true;
			this->label_scaling->Location = System::Drawing::Point(6, 29);
			this->label_scaling->Name = L"label_scaling";
			this->label_scaling->Size = System::Drawing::Size(71, 15);
			this->label_scaling->TabIndex = 23;
			this->label_scaling->Text = L"Scaling = \?";
			// 
			// label_theta
			// 
			this->label_theta->AutoSize = true;
			this->label_theta->Location = System::Drawing::Point(127, 29);
			this->label_theta->Name = L"label_theta";
			this->label_theta->Size = System::Drawing::Size(61, 15);
			this->label_theta->TabIndex = 24;
			this->label_theta->Text = L"Theta = \?";
			// 
			// label_difference
			// 
			this->label_difference->AutoSize = true;
			this->label_difference->Location = System::Drawing::Point(240, 29);
			this->label_difference->Name = L"label_difference";
			this->label_difference->Size = System::Drawing::Size(89, 15);
			this->label_difference->TabIndex = 25;
			this->label_difference->Text = L"Difference = \?";
			// 
			// label_before_image
			// 
			this->label_before_image->AutoSize = true;
			this->label_before_image->Location = System::Drawing::Point(260, 31);
			this->label_before_image->Name = L"label_before_image";
			this->label_before_image->Size = System::Drawing::Size(84, 15);
			this->label_before_image->TabIndex = 26;
			this->label_before_image->Text = L"Before Image";
			// 
			// label_after_image
			// 
			this->label_after_image->AutoSize = true;
			this->label_after_image->Location = System::Drawing::Point(921, 31);
			this->label_after_image->Name = L"label_after_image";
			this->label_after_image->Size = System::Drawing::Size(76, 15);
			this->label_after_image->TabIndex = 27;
			this->label_after_image->Text = L"After Image";
			// 
			// label_before_histogram
			// 
			this->label_before_histogram->AutoSize = true;
			this->label_before_histogram->Location = System::Drawing::Point(247, 505);
			this->label_before_histogram->Name = L"label_before_histogram";
			this->label_before_histogram->Size = System::Drawing::Size(108, 15);
			this->label_before_histogram->TabIndex = 28;
			this->label_before_histogram->Text = L"Before Histogram";
			// 
			// label_after_histogram
			// 
			this->label_after_histogram->AutoSize = true;
			this->label_after_histogram->Location = System::Drawing::Point(907, 505);
			this->label_after_histogram->Name = L"label_after_histogram";
			this->label_after_histogram->Size = System::Drawing::Size(100, 15);
			this->label_after_histogram->TabIndex = 29;
			this->label_after_histogram->Text = L"After Histogram";
			// 
			// radioButton_r_channel
			// 
			this->radioButton_r_channel->AutoSize = true;
			this->radioButton_r_channel->Location = System::Drawing::Point(10, 24);
			this->radioButton_r_channel->Name = L"radioButton_r_channel";
			this->radioButton_r_channel->Size = System::Drawing::Size(87, 19);
			this->radioButton_r_channel->TabIndex = 30;
			this->radioButton_r_channel->TabStop = true;
			this->radioButton_r_channel->Text = L"R Channel";
			this->radioButton_r_channel->UseVisualStyleBackColor = true;
			// 
			// radioButton_g_channel
			// 
			this->radioButton_g_channel->AutoSize = true;
			this->radioButton_g_channel->Location = System::Drawing::Point(135, 24);
			this->radioButton_g_channel->Name = L"radioButton_g_channel";
			this->radioButton_g_channel->Size = System::Drawing::Size(88, 19);
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
			this->groupBox_rgb_extraction->Location = System::Drawing::Point(1295, 103);
			this->groupBox_rgb_extraction->Name = L"groupBox_rgb_extraction";
			this->groupBox_rgb_extraction->Size = System::Drawing::Size(399, 91);
			this->groupBox_rgb_extraction->TabIndex = 32;
			this->groupBox_rgb_extraction->TabStop = false;
			// 
			// radioButton_grayscale
			// 
			this->radioButton_grayscale->AutoSize = true;
			this->radioButton_grayscale->Location = System::Drawing::Point(135, 49);
			this->radioButton_grayscale->Name = L"radioButton_grayscale";
			this->radioButton_grayscale->Size = System::Drawing::Size(83, 19);
			this->radioButton_grayscale->TabIndex = 34;
			this->radioButton_grayscale->TabStop = true;
			this->radioButton_grayscale->Text = L"Grayscale";
			this->radioButton_grayscale->UseVisualStyleBackColor = true;
			// 
			// radioButton_b_channel
			// 
			this->radioButton_b_channel->AutoSize = true;
			this->radioButton_b_channel->Location = System::Drawing::Point(10, 49);
			this->radioButton_b_channel->Name = L"radioButton_b_channel";
			this->radioButton_b_channel->Size = System::Drawing::Size(87, 19);
			this->radioButton_b_channel->TabIndex = 33;
			this->radioButton_b_channel->TabStop = true;
			this->radioButton_b_channel->Text = L"B Channel";
			this->radioButton_b_channel->UseVisualStyleBackColor = true;
			// 
			// groupBox_smooth_filter
			// 
			this->groupBox_smooth_filter->Controls->Add(this->radioButton_mean);
			this->groupBox_smooth_filter->Controls->Add(this->radioButton_median);
			this->groupBox_smooth_filter->Location = System::Drawing::Point(1295, 250);
			this->groupBox_smooth_filter->Name = L"groupBox_smooth_filter";
			this->groupBox_smooth_filter->Size = System::Drawing::Size(399, 59);
			this->groupBox_smooth_filter->TabIndex = 35;
			this->groupBox_smooth_filter->TabStop = false;
			// 
			// radioButton_mean
			// 
			this->radioButton_mean->AutoSize = true;
			this->radioButton_mean->Location = System::Drawing::Point(10, 24);
			this->radioButton_mean->Name = L"radioButton_mean";
			this->radioButton_mean->Size = System::Drawing::Size(60, 19);
			this->radioButton_mean->TabIndex = 30;
			this->radioButton_mean->TabStop = true;
			this->radioButton_mean->Text = L"Mean";
			this->radioButton_mean->UseVisualStyleBackColor = true;
			// 
			// radioButton_median
			// 
			this->radioButton_median->AutoSize = true;
			this->radioButton_median->Location = System::Drawing::Point(135, 24);
			this->radioButton_median->Name = L"radioButton_median";
			this->radioButton_median->Size = System::Drawing::Size(71, 19);
			this->radioButton_median->TabIndex = 30;
			this->radioButton_median->TabStop = true;
			this->radioButton_median->Text = L"Median";
			this->radioButton_median->UseVisualStyleBackColor = true;
			// 
			// radioButton_vertical
			// 
			this->radioButton_vertical->AutoSize = true;
			this->radioButton_vertical->Location = System::Drawing::Point(10, 24);
			this->radioButton_vertical->Name = L"radioButton_vertical";
			this->radioButton_vertical->Size = System::Drawing::Size(73, 19);
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
			this->groupBox_sobel_edge_detection->Location = System::Drawing::Point(1295, 536);
			this->groupBox_sobel_edge_detection->Name = L"groupBox_sobel_edge_detection";
			this->groupBox_sobel_edge_detection->Size = System::Drawing::Size(399, 59);
			this->groupBox_sobel_edge_detection->TabIndex = 36;
			this->groupBox_sobel_edge_detection->TabStop = false;
			// 
			// radioButton_combined
			// 
			this->radioButton_combined->AutoSize = true;
			this->radioButton_combined->Location = System::Drawing::Point(246, 24);
			this->radioButton_combined->Name = L"radioButton_combined";
			this->radioButton_combined->Size = System::Drawing::Size(86, 19);
			this->radioButton_combined->TabIndex = 35;
			this->radioButton_combined->TabStop = true;
			this->radioButton_combined->Text = L"Combined";
			this->radioButton_combined->UseVisualStyleBackColor = true;
			// 
			// radioButton_horizontal
			// 
			this->radioButton_horizontal->AutoSize = true;
			this->radioButton_horizontal->Location = System::Drawing::Point(128, 24);
			this->radioButton_horizontal->Name = L"radioButton_horizontal";
			this->radioButton_horizontal->Size = System::Drawing::Size(88, 19);
			this->radioButton_horizontal->TabIndex = 34;
			this->radioButton_horizontal->TabStop = true;
			this->radioButton_horizontal->Text = L"Horizontal";
			this->radioButton_horizontal->UseVisualStyleBackColor = true;
			// 
			// trackBar_defined_thresholding
			// 
			this->trackBar_defined_thresholding->Location = System::Drawing::Point(1295, 435);
			this->trackBar_defined_thresholding->Maximum = 255;
			this->trackBar_defined_thresholding->Name = L"trackBar_defined_thresholding";
			this->trackBar_defined_thresholding->Size = System::Drawing::Size(399, 56);
			this->trackBar_defined_thresholding->TabIndex = 38;
			this->trackBar_defined_thresholding->Value = 200;
			// 
			// label_control
			// 
			this->label_control->AutoSize = true;
			this->label_control->Location = System::Drawing::Point(1463, 31);
			this->label_control->Name = L"label_control";
			this->label_control->Size = System::Drawing::Size(50, 15);
			this->label_control->TabIndex = 39;
			this->label_control->Text = L"Control";
			// 
			// groupBox_image_registration
			// 
			this->groupBox_image_registration->Controls->Add(this->label_scaling);
			this->groupBox_image_registration->Controls->Add(this->label_theta);
			this->groupBox_image_registration->Controls->Add(this->label_difference);
			this->groupBox_image_registration->Location = System::Drawing::Point(1295, 833);
			this->groupBox_image_registration->Name = L"groupBox_image_registration";
			this->groupBox_image_registration->Size = System::Drawing::Size(399, 59);
			this->groupBox_image_registration->TabIndex = 40;
			this->groupBox_image_registration->TabStop = false;
			// 
			// groupBox_connected_component
			// 
			this->groupBox_connected_component->Controls->Add(this->label_connected_component);
			this->groupBox_connected_component->Location = System::Drawing::Point(1295, 712);
			this->groupBox_connected_component->Name = L"groupBox_connected_component";
			this->groupBox_connected_component->Size = System::Drawing::Size(399, 59);
			this->groupBox_connected_component->TabIndex = 41;
			this->groupBox_connected_component->TabStop = false;
			// 
			// label_connected_component
			// 
			this->label_connected_component->AutoSize = true;
			this->label_connected_component->Location = System::Drawing::Point(7, 24);
			this->label_connected_component->Name = L"label_connected_component";
			this->label_connected_component->Size = System::Drawing::Size(223, 15);
			this->label_connected_component->TabIndex = 23;
			this->label_connected_component->Text = L"Number of Connected Component = \?";
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 15);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(1727, 981);
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
			this->Name = L"MyForm";
			this->Text = L"MyForm";
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

	/* ==================================== Functional Button ==================================== */

	private: System::Void MyForm_Load(System::Object^  sender, System::EventArgs^  e) {

	}

	private: System::Void button_load_handler(System::Object^  sender, System::EventArgs^  e) {
		if (openImageWindow->ShowDialog() == System::Windows::Forms::DialogResult::OK) {
			originImage = gcnew Bitmap(openImageWindow->FileName);
			setPictureBox(pictureBox_before_image, originImage);
			setPictureBox(pictureBox_after_image, nullptr);
		}
	}

	private: System::Void button_undo_handler(System::Object^  sender, System::EventArgs^  e) {

	}

	private: void setPictureBox(PictureBox^ %pictureBox, Bitmap^ image) {
		pictureBox->Image = image;
	}

	private: bool isExist(Bitmap^ image) {
		return image != nullptr;
	}

	/* ==================================== Filter Method Button ==================================== */

	private: System::Void button_rgb_extraction_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

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

	}

	private: System::Void button_defined_thresholding_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		int threshold = trackBar_defined_thresholding->Value;

		transferImage = define_thresholding(originImage, threshold);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_sobel_edge_detection_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

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

		int threshold = trackBar_defined_thresholding->Value;

		transferImage = sobel_threshold_Combine(originImage, threshold);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_connected_component_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

		transferImage = connected_component(originImage);
		setPictureBox(pictureBox_after_image, transferImage);
	}

	private: System::Void button_image_registration_handler(System::Object^  sender, System::EventArgs^  e) {

		if (isExist(originImage) == false) {
			return;
		}

	}

};
}

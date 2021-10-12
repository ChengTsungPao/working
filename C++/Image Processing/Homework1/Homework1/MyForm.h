#include "ReadFile.h"
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
	private: System::Windows::Forms::Button^  button1;
	protected:
	private: System::Windows::Forms::Button^  button2;
	private: System::Windows::Forms::PictureBox^  pictureBox1;
	private: System::Windows::Forms::PictureBox^  pictureBox2;
	private: System::Windows::Forms::Button^  button3;

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
			this->button1 = (gcnew System::Windows::Forms::Button());
			this->button2 = (gcnew System::Windows::Forms::Button());
			this->pictureBox1 = (gcnew System::Windows::Forms::PictureBox());
			this->pictureBox2 = (gcnew System::Windows::Forms::PictureBox());
			this->button3 = (gcnew System::Windows::Forms::Button());
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox1))->BeginInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox2))->BeginInit();
			this->SuspendLayout();
			// 
			// button1
			// 
			this->button1->Location = System::Drawing::Point(12, 394);
			this->button1->Name = L"button1";
			this->button1->Size = System::Drawing::Size(143, 66);
			this->button1->TabIndex = 0;
			this->button1->Text = L"Load";
			this->button1->UseVisualStyleBackColor = true;
			this->button1->Click += gcnew System::EventHandler(this, &MyForm::button1_Click);
			// 
			// button2
			// 
			this->button2->Location = System::Drawing::Point(208, 394);
			this->button2->Name = L"button2";
			this->button2->Size = System::Drawing::Size(143, 66);
			this->button2->TabIndex = 1;
			this->button2->Text = L"Transfer";
			this->button2->UseVisualStyleBackColor = true;
			this->button2->Click += gcnew System::EventHandler(this, &MyForm::button2_Click);
			// 
			// pictureBox1
			// 
			this->pictureBox1->Location = System::Drawing::Point(12, 44);
			this->pictureBox1->Name = L"pictureBox1";
			this->pictureBox1->Size = System::Drawing::Size(414, 309);
			this->pictureBox1->TabIndex = 2;
			this->pictureBox1->TabStop = false;
			this->pictureBox1->Click += gcnew System::EventHandler(this, &MyForm::pictureBox1_Click);
			// 
			// pictureBox2
			// 
			this->pictureBox2->Location = System::Drawing::Point(448, 44);
			this->pictureBox2->Name = L"pictureBox2";
			this->pictureBox2->Size = System::Drawing::Size(414, 309);
			this->pictureBox2->TabIndex = 3;
			this->pictureBox2->TabStop = false;
			this->pictureBox2->Click += gcnew System::EventHandler(this, &MyForm::pictureBox2_Click);
			// 
			// button3
			// 
			this->button3->Location = System::Drawing::Point(403, 394);
			this->button3->Name = L"button3";
			this->button3->Size = System::Drawing::Size(143, 66);
			this->button3->TabIndex = 4;
			this->button3->Text = L"Next";
			this->button3->UseVisualStyleBackColor = true;
			this->button3->Click += gcnew System::EventHandler(this, &MyForm::button3_Click);
			// 
			// MyForm
			// 
			this->AutoScaleDimensions = System::Drawing::SizeF(8, 15);
			this->AutoScaleMode = System::Windows::Forms::AutoScaleMode::Font;
			this->ClientSize = System::Drawing::Size(1047, 747);
			this->Controls->Add(this->button3);
			this->Controls->Add(this->pictureBox2);
			this->Controls->Add(this->pictureBox1);
			this->Controls->Add(this->button2);
			this->Controls->Add(this->button1);
			this->Name = L"MyForm";
			this->Text = L"MyForm";
			this->Load += gcnew System::EventHandler(this, &MyForm::MyForm_Load);
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox1))->EndInit();
			(cli::safe_cast<System::ComponentModel::ISupportInitialize^>(this->pictureBox2))->EndInit();
			this->ResumeLayout(false);

		}
#pragma endregion
	private: Bitmap^ originImage;
	private: Bitmap^ transferImage;
	private: String^ path;
	private: int imageIndex;

	private: void setPictureBox(PictureBox^ %pictureBox, Bitmap^ image) {
		pictureBox->Image = image;
	}

	private: System::Void MyForm_Load(System::Object^  sender, System::EventArgs^  e) {

		imageIndex = 0;
		path = "..\\ExampleImage\\";

		vector<string> files = getFolderFiles(stringTransfer(path));
		originImage = readImage(path, stringTransfer(files[imageIndex]));
		setPictureBox(pictureBox1, originImage);

	}

	protected: System::Void button1_Click(System::Object^  sender, System::EventArgs^  e) {
		
		vector<string> files = getFolderFiles(stringTransfer(path));
		originImage = readImage(path, stringTransfer(files[imageIndex]));
		setPictureBox(pictureBox1, originImage);

	}

	private: System::Void button2_Click(System::Object^  sender, System::EventArgs^  e) {

		// transferImage = rgb_extraction_transformation(originImage, 'r');
		// transferImage = smooth_filter(originImage, 'm');
		// transferImage = define_thresholding(originImage);
		// transferImage = sobel_edge_dection(originImage, 'c');
		// transferImage = sobel_threshold_Combine(originImage);
		transferImage = connected_component(originImage);
		setPictureBox(pictureBox2, transferImage);

	}

	private: System::Void button3_Click(System::Object^  sender, System::EventArgs^  e) {
		imageIndex += 1;
		vector<string> files = getFolderFiles(stringTransfer(path));

		if (imageIndex == files.size()) {
			imageIndex = 0;
		}

		originImage = readImage(path, stringTransfer(files[imageIndex]));
		setPictureBox(pictureBox1, originImage);
		setPictureBox(pictureBox2, originImage);
		
	}

	private: System::Void pictureBox1_Click(System::Object^  sender, System::EventArgs^  e) {

	}

	private: System::Void pictureBox2_Click(System::Object^  sender, System::EventArgs^  e) {
	}

};
}

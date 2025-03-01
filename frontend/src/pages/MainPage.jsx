import React from "react";

const MainPage = () => {
  return (
    <main className="flex flex-col items-center bg-[rgb(248,249,250)]">
      <div className="flex justify-between w-full bg-white h-[446px] mt-[112px]">
        <div className="pl-8">
          <p className="text-[60px] font-[roboto-bold]">
            Welcome to
            <br />
            KW Chat Bot
          </p>
          <p className="mt-5 w-[561px] text-[20px] text-[#6B7280;]">
            Your intelligent assistant for all college-related information. Get
            instant answers about admissions, courses, campus life, and more.
          </p>
          <div className="flex gap-3 mt-8 text-[18px]">
            <a href="/chat">
              <button className="px-[41px] h-[62px] bg-black rounded-[4px] text-white duration-100 hover:scale-110">
                Start Chatting
              </button>
            </a>
            <a href="/faq">
              <button className="px-[41px] h-[62px] bg-[#E0E7FF] rounded-[4px] text-black duration-100 hover:scale-110">
                View FAQ
              </button>
            </a>
          </div>
        </div>
        <div className="w-[720px] h-[446px] relative">
          <img
            src="assets/Main/robot.png"
            className="w-[720px] h-full object-cover"
          />
        </div>
      </div>
      <div className="w-full h-[288px] py-[48px] px-[80px] flex flex-col items-center">
        <p className="text-[16px] font-[roboto-bold]">Features</p>
        <p className="mt-2 text-[36px] font-[roboto-bold]">
          Everything you need to know
        </p>
        <div className="mt-[40px] w-full h-[80px] flex justify-between">
          <div className="flex items-start gap-4">
            <div className="relative bg-black w-[48px] h-[48px] aspect-square rounded-[6px] flex justify-center items-center">
              <img src="assets/Main/HaksaMo.png" />
            </div>
            <div className="flex flex-col gap-2">
              <p className="text-[18px] font-[roboto-bold]">
                Admission Information
              </p>
              <p className="w-[295px] text-[16px] text-[#6B7280]">
                Get detailed information about admission requirements,
                deadlines, and processes.{" "}
              </p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="relative bg-black w-[48px] h-[48px] aspect-square rounded-[6px] flex justify-center items-center">
              <img src="assets/Main/Book.png" />
            </div>
            <div className="flex flex-col gap-2">
              <p className="text-[18px] font-[roboto-bold]">Course Guidance</p>
              <p className="w-[295px] text-[16px] text-[#6B7280]">
                Explore course offerings, prerequisites, and program
                requirements.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-4">
            <div className="relative bg-black w-[48px] h-[48px] aspect-square rounded-[6px] flex justify-center items-center">
              <img src="assets/Main/People.png" />
            </div>
            <div className="flex flex-col gap-2">
              <p className="text-[18px] font-[roboto-bold]">Campus Life</p>
              <p className="w-[295px] text-[16px] text-[#6B7280]">
                Learn about student activities, housing, and campus facilities.
              </p>
            </div>
          </div>
        </div>
      </div>
      <div className="bg-white py-[48px] px-[112px] w-full flex justify-center items-center flex-col">
        <p className="text-[36px] font-[roboto-bold]">
          Frequently Asked Questions
        </p>
        <p className="text-[18px] text-[#6B7280] mt-[28px]">
          Can't find the answer you're looking for? Contact our support team.{" "}
        </p>
        <div className="flex flex-col gap-8 w-full items-center mt-[50px]">
          <div className="w-[768px] h-[200px] bg-[rgb(248,249,250)] rounded-[8px] flex flex-col items-center p-[24px]">
            <div className="flex w-full justify-center items-center">
              <input
                type="checkbox"
                className="hidden peer"
                id="main-checkbox-1"
              />
              <p className="text-[18px] font-[roboto-bold] ml-auto">
                공학 인증 제도란 무엇인가요?
              </p>
              <div className="relative ml-auto">
                <img src="assets/Main/DownArrow.png" />
              </div>
            </div>
            <p className="text-[16px] text-[#6B7280] mt-[19px] mb-4">
              광운대학교의 공학교육인증제도는 한국공학교육인증원(ABEEK)의 평가를
              통해, 해당 교육과정을 이수한 졸업생이 산업체의 요구와 글로벌
              스탠더드를 만족하는 인재임을 보장하는 제도입니다. 이를 통해
              졸업생은 국제적으로 전문 엔지니어로 인정받을 수 있으며, 국내 주요
              기업에서 가산점 혜택을 받을 수 있습니다.
            </p>
            <div className="flex gap-[15.8px] w-full text-[14px]">
              <div className="flex items-center gap-[7.81px] text-[#6B7280]">
                <div className="relative">
                  <img
                    src="/assets/Main/Up.png"
                    className="duration-100 hover:scale-105"
                  />
                </div>
                <p>Helpful</p>
              </div>{" "}
              <div className="flex items-center gap-[7.81px] text-[#6B7280]">
                <div className="relative">
                  <img
                    src="/assets/Main/Down.png"
                    className="duration-100 hover:scale-105"
                  />
                </div>
                <p>Not helpful </p>
              </div>
            </div>
          </div>
        </div>
        <div className="flex flex-col gap-8 w-full items-center mt-[50px]">
          <div className="w-[768px] h-[200px] bg-[rgb(248,249,250)] rounded-[8px] flex flex-col items-center p-[24px]">
            <div className="flex w-full justify-center items-center">
              <p className="text-[18px] font-[roboto-bold] ml-auto">
                학과별 졸업 요건을 어디에서 찾을 수 있을까요?
              </p>
              <div className="relative ml-auto">
                <img src="assets/Main/DownArrow.png" />
              </div>
            </div>
            <p className="text-[16px] text-[#6B7280] mt-[19px] mb-4">
              학교 홈페이지 연결 링크 :
              <a
                href="https://www.kw.ac.kr/ko/life/bachelor_info07.jsp"
                className="hover:text-blue-600 hover:underline hover:underline-offset-1 hover:decoration-blue-600"
              >
                https://www.kw.ac.kr/ko/life/bachelor_info07.jsp
              </a>
            </p>
            <div
              className="flex gap-[15.8px] w-full text-[14px] mt-auto
        "
            >
              <div className="flex items-center gap-[7.81px] text-[#6B7280]">
                <div className="relative">
                  <img
                    src="/assets/Main/Up.png"
                    className="duration-100 hover:scale-105"
                  />
                </div>
                <p>Helpful</p>
              </div>{" "}
              <div className="flex items-center gap-[7.81px] text-[#6B7280]">
                <div className="relative">
                  <img
                    src="/assets/Main/Down.png"
                    className="duration-100 hover:scale-105"
                  />
                </div>
                <p>Not helpful </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default MainPage;

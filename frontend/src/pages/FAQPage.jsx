import React from "react";

const FAQPage = () => {
  return (
    <main className="flex-grow pt-20 pb-16 max-w-8xl mx-auto px-4 sm:px-6 lg:px-8">
      <p className="text-[36px] font-[roboto-bold]">
        Frequently asked questions.
      </p>
      <p className="mt-4 text-[20px] text-[#4B5563]">
        Your personal assistant for all college-related information and guidance
      </p>
      <a href="/chat">
        <button className="mt-8 w-[278.96px] h-[60px] bg-black text-white rounded-[4px] flex items-center justify-center gap-2 hover:ring-2 hover:ring-offset-1 ring-black">
          <div className="relative">
            <img src="assets/FaQ/miniRobot.png" />
          </div>
          <p>Start Chat with KW Bot </p>
        </button>
      </a>

      <div className="mt-[64px] w-full h-full flex flex-col px-[32px]">
        <div className="flex gap-6">
          <div className="w-[326px] h-[160px] bg-white shadow rounded-8px p-6 flex flex-col gap-3 rounded">
            <div className="flex gap-2 items-center">
              <div className="relative">
                <img src="assets/FaQ/HakSaMo3.png" />
              </div>
              <p className="text-[18px] font-[roboto-bold]">
                졸업 요건 상세 페이지
              </p>
            </div>
            <a
              className="text-[#4B5563] text-[16px] hover:text-blue-600 hover:underline hover:underline-offset-1 hover:decoration-blue-600"
              href="https://www.kw.ac.kr/ko/life/bachelor_info07.jsp"
            >
              https://www.kw.ac.kr/ko/life/bachelor_ info07.jsp
            </a>
          </div>
          <div className="w-[326px] h-[160px] bg-white shadow rounded-8px p-6 flex flex-col gap-3 rounded">
            <div className="flex gap-2 items-center">
              <div className="relative">
                <img src="assets/FaQ/Calendar.png" />
              </div>
              <p className="text-[18px] font-[roboto-bold]">
                광운대학교 홈페이지
              </p>
            </div>
            <a
              className="text-[#4B5563] text-[16px] hover:text-blue-600 hover:underline hover:underline-offset-1 hover:decoration-blue-600"
              href="https://www.kw.ac.kr/ko/index.jsp"
            >
              https://www.kw.ac.kr/ko/index.jsp
            </a>
          </div>
          <div className="w-[326px] h-[160px] bg-white shadow rounded-8px p-6 flex flex-col gap-3 rounded">
            <div className="flex gap-2 items-center">
              <div className="relative">
                <img src="assets/FaQ/Note.png" />
              </div>
              <p className="text-[18px] font-[roboto-bold]">
                광운대학교 근처 맛집 정보 영상
              </p>
            </div>
            <a
              className="text-[#4B5563] text-[16px] hover:text-blue-600 hover:underline hover:underline-offset-1 hover:decoration-blue-600"
              href="https://www.youtube.com/watch?v=Iw21UhFpl3c"
            >
              https://www.youtube.com/watch?v= ZLg6ZjJsMWY
            </a>
          </div>
          <div className="w-[326px] h-[160px] bg-white shadow rounded-8px p-6 flex flex-col gap-3 rounded">
            <div className="flex gap-2 items-center">
              <div className="relative">
                <img src="assets/FaQ/People2.png" />
              </div>
              <p className="text-[18px] font-[roboto-bold]">
                공학인증 관련 안내 페이지
              </p>
            </div>
            <a
              className="text-[#4B5563] text-[16px] hover:text-blue-600 hover:underline hover:underline-offset-1 hover:decoration-blue-600"
              href="https://www.kw.ac.kr/ko/life/bachelor_info09.jsp"
            >
              https://ce.kw.ac.kr/engi neering_certify/engineering_certify.php
            </a>
          </div>
        </div>
        <div className=" h-[178px] bg-white shadow rounded-8px p-6 flex flex-col gap-3 mt-[48px] rounded w-full">
          <div className="flex gap-2 items-center">
            <p className="text-[24px] font-[roboto-bold]">Quick Access Links</p>
          </div>
          <a
            className="w-[310px] h-[58px] border rounded-[8px] border-[#E5E7EB] p-5 flex gap-2 items-center hover:bg-gray-200"
            href="https://www.topcit.or.kr/home.do"
          >
            <div className="relative">
              <img src="assets/FaQ/Note2.png" />
            </div>
            <p>TOPCIT 에 대하여</p>
          </a>
        </div>
      </div>
    </main>
  );
};

export default FAQPage;

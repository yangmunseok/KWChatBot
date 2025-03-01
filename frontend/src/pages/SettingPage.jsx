import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import React, { useRef, useState } from "react";
import { toast } from "react-toastify";

const SettingPage = () => {
  const klasForm = useRef({ id: "", password: "" });
  const toastId = useRef();
  const majorTypesOption = useRef();
  const majorTypes = [
    "단일 전공",
    "심화 전공",
    "복수 전공",
    "연계 전공",
    "학생설계융합 전공",
    "마이크로 전공",
  ];
  const queryClient = useQueryClient();

  const { data: studentData, isPending: studentPending } = useQuery({
    queryKey: ["studentData"],
    queryFn: async () => {
      try {
        const res = await fetch("api/student/getStudentInfo");
        const data = await res.json();
        if (!res.ok) {
          throw new Error(
            data.detail?.error || data.error || "Something wend wrong!"
          );
        }
        return data;
      } catch (error) {
        throw new Error(error);
      }
    },
    refetchOnWindowFocus: false,
    retry: false,
  });

  const { mutate: majorMutation } = useMutation({
    mutationFn: async () => {
      try {
        const majorType = majorTypesOption.current.value;
        console.log("majorType: ", majorType);
        const res = await fetch("api/student/setStudentMajorType", {
          method: "POST",
          headers: { "Content-type": "application/json" },
          body: JSON.stringify({ major_type: majorType }),
        });
        if (!res.ok) {
          throw new Error(
            data.detail?.error || data.error || "Something wend wrong!"
          );
        }
      } catch (error) {
        throw new Error(error);
      }
    },
  });

  const {
    mutate: crawlMutaion,
    isError,
    error,
    isPending: crawlPending,
  } = useMutation({
    mutationFn: async () => {
      try {
        const res = await fetch("api/student/setStudentInfo", {
          method: "POST",
          headers: { "Content-type": "application/json" },
          body: JSON.stringify({
            id: klasForm.current.id,
            password: klasForm.current.password,
          }),
        });
        const data = await res.json();
        console.log("data:", data);
        if (!res.ok) {
          throw new Error(
            data.detail?.error || data.error || "Something wend wrong!"
          );
        }
      } catch (error) {
        throw new Error(error);
      }
    },
    onSuccess: () => {
      queryClient.invalidateQueries(["studentData"]);
      toast.success("Crawling completed!");
    },
    onError: () => {
      toast.error("Crawling failed.");
    },
    onMutate: () => {
      toastId.current = toast.loading("Crawling...");
    },
    onSettled: () => {
      toast.dismiss(toastId.current);
      toastId.current = null;
    },
  });
  if (studentPending) {
    return (
      <div class="h-screen w-full py-20 relative flex md:flex-row flex-col gap-10 justify-center items-center bg-white">
        <div class="border-gray-300 h-20 w-20 animate-spin rounded-full border-8 border-t-blue-600" />
      </div>
    );
  }

  return (
    <main class="flex-grow pt-16">
      <div class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="space-y-8">
          <section class="bg-white shadow rounded-lg p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-6">Edit Profile</h2>
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Major Type
                </label>
                <select
                  class="mt-1 block w-full !rounded-button border-gray-300 shadow-sm"
                  ref={majorTypesOption}
                  defaultValue={studentData["전공 타입"] || "단일 전공"}
                >
                  {majorTypes.map((major) => (
                    <option key={major}>{major}</option>
                  ))}
                </select>
              </div>
            </div>
          </section>

          <section class="bg-white shadow rounded-lg p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-6">
              AI Model Configuration
            </h2>
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Language Model
                </label>
                <select class="mt-1 block w-full !rounded-button border-gray-300 shadow-sm">
                  <option>GPT-4</option>
                  <option>GPT-3.5</option>
                  <option>DeepSeek</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Maximum Response Length
                </label>
                <input
                  type="range"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  min="100"
                  max="2000"
                />
                <div class="mt-1 text-sm text-gray-500">1000 tokens</div>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  Temperature (Creativity)
                </label>
                <input
                  type="range"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                  min="0"
                  max="100"
                />
                <div class="mt-1 text-sm text-gray-500">0.7</div>
              </div>
            </div>
          </section>

          <section class="bg-white shadow rounded-lg p-6">
            <h2 class="text-lg font-medium text-gray-900 mb-6">
              Crawling Setting
            </h2>
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700">
                  KLAS User Info
                </label>
                <div class="mt-2 space-y-2">
                  <input
                    type="text"
                    class="block rounded-lg"
                    placeholder="ID"
                    onChange={(e) => {
                      klasForm.current.id = e.target.value;
                    }}
                  />
                  <input
                    type="password"
                    class="block rounded-lg"
                    placeholder="PASSWORD"
                    onChange={(e) => {
                      klasForm.current.password = e.target.value;
                    }}
                  />
                  <span class="ml-2 text-sm text-gray-700">
                    We do not store or misuse user data.
                  </span>
                </div>
              </div>
              <div>
                <button
                  onClick={crawlMutaion}
                  class="!rounded-button text-white px-4 py-2 text-sm font-medium bg-custom hover:bg-custom/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-custom"
                >
                  Crawl
                </button>
                {isError && (
                  <p className="text-sm text-red-700 mt-1">{error.message}</p>
                )}
              </div>
            </div>
          </section>
          <button
            onClick={majorMutation}
            class="!rounded-button text-white px-4 py-2 text-sm font-medium bg-purple-600 hover:bg-purple-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            Save
          </button>
        </div>
      </div>
    </main>
  );
};

export default SettingPage;

import { NextResponse } from 'next/server';

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const SARVAM_API_KEY = process.env.SARVAM_API_KEY;

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const userQuery = body.message || body.query || "";
    const requestedLang = body.language || "auto";

    if (!userQuery.trim()) {
      return NextResponse.json({ error: "Empty query" }, { status: 400 });
    }

    // Default farm context
    const farmContext = `
Current Vermicomposting Farm Status (Vermikendra Site Pune):
- BED-01: NORMAL (Moisture 65%, Temp 26°C, Harvest Stage: Day 42/60, Harvest ready in ~10 days. Castings look dark and earthy.)
- BED-02: NORMAL (Moisture 64%, Temp 27°C, Good earthworm activity.)
- BED-03: WATCH (Temp 34.2°C - trending HOT! High core heat risks killing worms. Action: Loosen top 4 inches with fork, pull shade net, light water mist.)
- BED-04: NORMAL (Moisture 62%, Temp 28°C, Healthy.)
- BED-05: ACTION_NEEDED (Moisture 42% - CRITICALLY DRY! Worms are suffocating in dry soil. Action: Immediately sprinkle 2 big buckets / 35-40L of water and cover with damp gunny bag / बोरा.)
- BED-06: OFFLINE (Sensor not responding for 1 hour).
`;

    const systemPrompt = `You are 'Vermi' (वर्मी), an affectionate and practical agronomist advising an Indian vermicomposting farmer in real time.
Farmer query: "${userQuery}"

Rules:
1. Always respond in the EXACT same language the farmer uses.
   - If the query is in Marathi, reply in natural Marathi (मराठी).
   - If in Hindi or Hinglish, reply in friendly Hindi (हिंदी).
   - If in English, reply in simple, clear English.
2. Ground your advice in the live bed status:
${farmContext}
3. Speak in practical physical actions a farmer understands (e.g. "2 बादल्या पाणी", "ओले पोते / गोणपाट झाका", "पंझाने हलके भुसभुशीत करा", "उन्हापासून शेडनेट टाका"). Do not use technical jargon like "volumetric water content".
4. Keep the answer concise (2-4 clear sentences) so it sounds natural when spoken aloud over phone speaker.`;

    let replyText = "";

    // 1. Call Gemini 2.5 Flash if key available
    if (GEMINI_API_KEY) {
      try {
        const geminiRes = await fetch(
          `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              contents: [{ parts: [{ text: systemPrompt }] }],
              generationConfig: {
                maxOutputTokens: 250,
                temperature: 0.3
              }
            })
          }
        );

        if (geminiRes.ok) {
          const geminiData = await geminiRes.json();
          replyText = geminiData.candidates?.[0]?.content?.parts?.[0]?.text?.trim() || "";
        }
      } catch (err) {
        console.error("Gemini API error:", err);
      }
    }

    // Fallback if Gemini fails or is offline
    if (!replyText) {
      const q = userQuery.toLowerCase();
      if (q.includes("bed 5") || q.includes("bed-5") || q.includes("पाणी") || q.includes("water") || q.includes("dry")) {
        replyText = "बेड क्रमांक ५ मध्ये ओलावा ४२% वर घसरला आहे. कृपया ताबडतोब दोन मोठ्या बादल्या (सुमारे ३५-४० लिटर) पाणी शिंपडा आणि ओल्या गोणपाटाने झाकून ठेवा.";
      } else if (q.includes("bed 3") || q.includes("temp") || q.includes("गरम") || q.includes("heat")) {
        replyText = "बेड क्रमांक ३ मध्ये तापमान ३४ अंश सेल्सिअसच्या वर गेले आहे. गांडुळांना वाचवण्यासाठी वरचा थर पंजाने भुसभुशीत करा आणि शेडनेट ओढून सावली करा.";
      } else if (q.includes("harvest") || q.includes("खत") || q.includes("तयार")) {
        replyText = "बेड क्रमांक १ चे खत काळेभोर आणि चहाच्या पावडरसारखे तयार होत आले आहे. काढणीच्या ३ दिवस आधी पाणी देणे थांबवा, म्हणजे गांडूळ खाली जातील.";
      } else {
        replyText = "वर्मीकेंद्रामध्ये आपले ६ बेड आहेत. बेड ५ ला तात्काळ पाण्याची गरज आहे आणि बेड ३ गरम होत आहे. इतर सर्व बेडची गांडूळ क्रिया सुरळीत आहे.";
      }
    }

    // 2. Synthesize Audio via Sarvam AI TTS if key available
    let audioBase64: string | null = null;
    if (SARVAM_API_KEY && replyText) {
      try {
        // Detect language
        const isMarathi = /[\u0900-\u097F]/.test(replyText) && (replyText.includes("आहे") || replyText.includes("करा") || replyText.includes("बेड"));
        const targetLang = isMarathi ? "mr-IN" : "hi-IN";
        const speaker = isMarathi ? "soham" : "aditya";

        const sarvamRes = await fetch("https://api.sarvam.ai/text-to-speech", {
          method: "POST",
          headers: {
            "api-subscription-key": SARVAM_API_KEY,
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            inputs: [replyText.slice(0, 450)],
            target_language_code: targetLang,
            speaker: speaker,
            model: "bulbul:v3"
          })
        });

        if (sarvamRes.ok) {
          const sarvamData = await sarvamRes.json();
          if (sarvamData.audios && sarvamData.audios.length > 0) {
            audioBase64 = sarvamData.audios[0];
          }
        }
      } catch (ttsErr) {
        console.error("Sarvam TTS error:", ttsErr);
      }
    }

    return NextResponse.json({
      text: replyText,
      audio_base64: audioBase64,
      provider: audioBase64 ? "gemini-2.5-flash + sarvam-bulbul-v3" : "gemini-2.5-flash"
    });

  } catch (error: any) {
    console.error("Assistant API handler error:", error);
    return NextResponse.json({ error: "Internal assistant error" }, { status: 500 });
  }
}

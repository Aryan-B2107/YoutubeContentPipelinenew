This package takes in raw transcript data, redirects it to:

1)LLM1 (Chunker LLM):
which chunks the transcripts as per jokes start and end time stamps

2)LLM2 (Scorer LLM):
this call to the gemini API service takes the chunked transcripts and scores all
the transcripts and sorts it as per score

Scoring metrics:
1)humour score
2)relatibility score(to audience)
3)shock value
4)tone summary
5)virality score-(fine tune on other metrics)

3. LLM3 (multiple Sound effects assigned  as per time stamp)

This LLM pass takes in the input individually chunked input transcripts, analyses audience pauses, laughs,
highs and lows to eventually selects from 100s of audio sound effects from

url = examplemp3s.com  assign sound effects to timestamps

after entire pass, audio files associated to correct timestamps will be 
stitched using the compositing module(ffmpeg)

क्या नाम है तेरा यवनिका यवनिका मम्मी ने रखा है ले ठीक है तेरा कोई भाई बहन है हां - 0
उसका क्या नाम है शारद
लिका बोल रहा है मंजुलिका
[संगीत] कहां पे रहते हो आप मस्जिद बंद है अरे भाई
तो सुनो ना मेरे फोन का डिस्प्ले क्या है वो लग रहा है ना सलमान का जो ब्रेसलेट है वही टाइप का लग रहा है हां उसका ही आता
लेके आई फार्म हाउस प गई थी - 2
क्या मैं चाहता हूं हनी सिंह के फैंस ना डोरेमोन को कपड़े पहन के जाए और लेजर मारे
क्योंकि जियान की एक ही गैड से भरती
[संगीत] है चलो
बढ़िया चालू करें हां रे बे मुजरा होने वाला है क्या हां करो
चालू कौन हसा इतनी जोर से हसो हसो भाई इतना भी मत हसना कि लोग लिख दे पेड ऑडियंस
हां कुछ लोग हसते हैं भाई तू क्या बैग बैग एकदम गोदी में पता न
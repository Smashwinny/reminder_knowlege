import runpy
import unittest
from pathlib import Path

NS = runpy.run_path(str(Path(__file__).with_name("listening_loop.py")))


class ListeningLoopTests(unittest.TestCase):
    def test_word_error_rate(self):
        metrics = NS["word_metrics"]("a b c d", "a x c d")
        self.assertEqual(metrics["word_edits"], 1)
        self.assertEqual(metrics["word_error_rate"], 0.25)
        self.assertEqual(metrics["word_accuracy_proxy"], 0.75)

    def test_key_points(self):
        result = NS["key_point_coverage"]("The project is late and a task blocked me")
        self.assertEqual(result["hits"], [True, True, False])
        self.assertAlmostEqual(result["score_proxy"], 2 / 3, places=3)

    def test_chunk_recycling(self):
        result = NS["chunk_recycling"](["I explain which task blocked me."])
        self.assertEqual(result["score_proxy"], 0.3333)

    def test_error_category_rejected(self):
        with self.assertRaises(ValueError):
            NS["validate_errors"]("blocked", "locked", [{"original": "blocked", "heard": "locked", "category": " guessed "}])

    def test_review_does_not_reteach_covered_key_points(self):
        recycled = NS["chunk_recycling"](["which task blocked me"])
        retell = {"hits": [True, True, True]}
        questions = NS["build_review_questions"]([], recycled, retell)
        self.assertFalse(any("复述关键点" in question for question in questions))

    def test_audio_is_real_nonempty_wav(self):
        from array import array
        import math
        import sys
        import wave
        path = Path(__file__).with_name("material.wav")
        with wave.open(str(path), "rb") as wav:
            self.assertEqual(wav.getnchannels(), 1)
            self.assertEqual(wav.getsampwidth(), 2)
            self.assertGreater(wav.getnframes(), 16000)
            samples = array("h", wav.readframes(wav.getnframes()))
            if sys.byteorder != "little":
                samples.byteswap()
            rms = math.sqrt(sum(sample * sample for sample in samples) / len(samples))
            self.assertGreater(rms, 100)


if __name__ == "__main__":
    unittest.main(verbosity=2)

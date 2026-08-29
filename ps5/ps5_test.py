# 6.00
# Problem Set 5 Test Suite
from io import BytesIO
from pathlib import Path
import tempfile
import unittest

import feedparser
from project_util import translate_html
from ps5 import *
from datetime import timedelta


class ProblemSet5NewsStory(unittest.TestCase):
    def setUp(self):
        pass

    def testNewsStoryConstructor(self):
        story = NewsStory('', '', '', '', datetime.now())

    def testNewsStoryGetGuid(self):
        story = NewsStory('test guid', 'test title', 
                          'test description', 'test link', datetime.now())
        self.assertEqual(story.get_guid(), 'test guid')

    def testNewsStoryGetTitle(self):
        story = NewsStory('test guid', 'test title', 
                          'test description', 'test link', datetime.now())
        self.assertEqual(story.get_title(), 'test title')

    def testNewsStoryGetdescription(self):
        story = NewsStory('test guid', 'test title', 
                          'test description', 'test link', datetime.now())
        self.assertEqual(story.get_description(), 'test description')

    def testNewsStoryGetLink(self):
        story = NewsStory('test guid', 'test title', 
                          'test description', 'test link', datetime.now())
        self.assertEqual(story.get_link(), 'test link')

    def testNewsStoryGetTime(self):
        story = NewsStory('test guid', 'test title', 
                          'test description', 'test link', datetime.now())
        self.assertEqual(type(story.get_pubdate()), datetime)
        
class ProblemSet5(unittest.TestCase):
    def setUp(self):
        class TrueTrigger:
            def evaluate(self, story): return True

        class FalseTrigger:
            def evaluate(self, story): return False

        self.tt = TrueTrigger()
        self.tt2 = TrueTrigger()
        self.ft = FalseTrigger()
        self.ft2 = FalseTrigger()

    def test1TitleTrigger(self):
        cuddly    = NewsStory('', 'The purple cow is soft and cuddly.', '', '', datetime.now())
        exclaim   = NewsStory('', 'Purple!!! Cow!!!', '', '', datetime.now())
        symbols   = NewsStory('', 'purple@#$%cow', '', '', datetime.now())
        spaces    = NewsStory('', 'Did you see a purple     cow?', '', '', datetime.now())
        caps      = NewsStory('', 'The farmer owns a really PURPLE cow.', '', '', datetime.now())
        exact     = NewsStory('', 'purple cow', '', '', datetime.now())

        plural    = NewsStory('', 'Purple cows are cool!', '', '', datetime.now())
        separate  = NewsStory('', 'The purple blob over there is a cow.', '', '', datetime.now())
        brown     = NewsStory('', 'How now brown cow.', '' ,'', datetime.now())
        badorder  = NewsStory('', 'Cow!!! Purple!!!', '', '', datetime.now())
        nospaces  = NewsStory('', 'purplecowpurplecowpurplecow', '', '', datetime.now())
        nothing   = NewsStory('', 'I like poison dart frogs.', '', '', datetime.now())

        s1 = TitleTrigger('PURPLE COW')
        s2  = TitleTrigger('purple cow')
        for trig in [s1, s2]:
            self.assertTrue(trig.evaluate(cuddly), "TitleTrigger failed to fire when the phrase appeared in the title.")
            self.assertTrue(trig.evaluate(exclaim), "TitleTrigger failed to fire when the words were separated by exclamation marks.")
            self.assertTrue(trig.evaluate(symbols), "TitleTrigger failed to fire when the words were separated by assorted punctuation.")
            self.assertTrue(trig.evaluate(spaces), "TitleTrigger failed to fire when the words were separated by multiple spaces.")
            self.assertTrue(trig.evaluate(caps), "TitleTrigger failed to fire when the phrase appeared with both uppercase and lowercase letters.")
            self.assertTrue(trig.evaluate(exact), "TitleTrigger failed to fire when the words in the phrase were the only words in the title.")
            
            self.assertFalse(trig.evaluate(plural), "TitleTrigger fired when the words in the phrase were contained within other words.")
            self.assertFalse(trig.evaluate(separate), "TitleTrigger fired when the words in the phrase were separated by other words.")
            self.assertFalse(trig.evaluate(brown), "TitleTrigger fired when only part of the phrase was found.")
            self.assertFalse(trig.evaluate(badorder), "TitleTrigger fired when the words in the phrase appeared out of order.")
            self.assertFalse(trig.evaluate(nospaces), "TitleTrigger fired when words were not separated by spaces or punctuation.")
            self.assertFalse(trig.evaluate(nothing), "TitleTrigger fired when none of the words in the phrase appeared.")

    def test2DescriptionTrigger(self):
        cuddly    = NewsStory('', '', 'The purple cow is soft and cuddly.', '', datetime.now())
        exclaim   = NewsStory('', '', 'Purple!!! Cow!!!', '', datetime.now())
        symbols   = NewsStory('', '', 'purple@#$%cow', '', datetime.now())
        spaces    = NewsStory('', '', 'Did you see a purple     cow?', '', datetime.now())
        caps      = NewsStory('', '', 'The farmer owns a really PURPLE cow.', '', datetime.now())
        exact     = NewsStory('', '', 'purple cow', '', datetime.now())

        plural    = NewsStory('', '', 'Purple cows are cool!', '', datetime.now())
        separate  = NewsStory('', '', 'The purple blob over there is cow.', '', datetime.now())
        brown     = NewsStory('', '', 'How now brown cow.', '', datetime.now())
        badorder  = NewsStory('', '', 'Cow!!! Purple!!!', '', datetime.now())
        nospaces  = NewsStory('', '', 'purplecowpurplecowpurplecow', '', datetime.now())
        nothing   = NewsStory('', '', 'I like poison dart frogs.', '', datetime.now())

        s1 = DescriptionTrigger('PURPLE COW')
        s2  = DescriptionTrigger('purple cow')
        for trig in [s1, s2]:
            self.assertTrue(trig.evaluate(cuddly), "DescriptionTrigger failed to fire when the phrase appeared in the description.")
            self.assertTrue(trig.evaluate(exclaim), "DescriptionTrigger failed to fire when the words were separated by exclamation marks.")
            self.assertTrue(trig.evaluate(symbols), "DescriptionTrigger failed to fire when the words were separated by assorted punctuation.")
            self.assertTrue(trig.evaluate(spaces), "DescriptionTrigger failed to fire when the words were separated by multiple spaces.")
            self.assertTrue(trig.evaluate(caps), "DescriptionTrigger failed to fire when the phrase appeared with both uppercase and lowercase letters.")
            self.assertTrue(trig.evaluate(exact), "DescriptionTrigger failed to fire when the words in the phrase were the only words in the description.")
            
            self.assertFalse(trig.evaluate(plural), "DescriptionTrigger fired when the words in the phrase were contained within other words.")
            self.assertFalse(trig.evaluate(separate), "DescriptionTrigger fired when the words in the phrase were separated by other words.")
            self.assertFalse(trig.evaluate(brown), "DescriptionTrigger fired when only part of the phrase was found.")
            self.assertFalse(trig.evaluate(badorder), "DescriptionTrigger fired when the words in the phrase appeared out of order.")
            self.assertFalse(trig.evaluate(nospaces), "DescriptionTrigger fired when words were not separated by spaces or punctuation.")
            self.assertFalse(trig.evaluate(nothing), "DescriptionTrigger fired when none of the words in the phrase appeared.")

    def test3altBeforeAndAfterTrigger(self):

        dt = timedelta(seconds=5)
        now = datetime(2016, 10, 12, 23, 59, 59)
        now = now.replace(tzinfo=pytz.timezone("EST"))
        
        ancient_time = datetime(1987, 10, 15)
        ancient_time = ancient_time.replace(tzinfo=pytz.timezone("EST"))
        ancient = NewsStory('', '', '', '', ancient_time)
        
        just_now = NewsStory('', '', '', '', now - dt)
        in_a_bit = NewsStory('', '', '', '', now + dt)
        
        future_time = datetime(2087, 10, 15)
        future_time = future_time.replace(tzinfo=pytz.timezone("EST"))
        future = NewsStory('', '', '', '', future_time)


        s1 = BeforeTrigger('12 Oct 2016 23:59:59')
        s2 = AfterTrigger('12 Oct 2016 23:59:59')

        self.assertTrue(s1.evaluate(ancient), "BeforeTrigger failed to fire on news from long ago")
        self.assertTrue(s1.evaluate(just_now), "BeforeTrigger failed to fire on news happened right before specified time")

        self.assertFalse(s1.evaluate(in_a_bit), "BeforeTrigger fired to fire on news happened right after specified time")
        self.assertFalse(s1.evaluate(future), "BeforeTrigger fired to fire on news from the future")

        self.assertFalse(s2.evaluate(ancient), "AfterTrigger fired to fire on news from long ago")
        self.assertFalse(s2.evaluate(just_now), "BeforeTrigger fired to fire on news happened right before specified time")

        self.assertTrue(s2.evaluate(in_a_bit), "AfterTrigger failed to fire on news just after specified time")
        self.assertTrue(s2.evaluate(future), "AfterTrigger failed to fire on news from long ago")

    def test3BeforeAndAfterTrigger(self):

        dt = timedelta(seconds=5)
        now = datetime(2016, 10, 12, 23, 59, 59)
        ancient = NewsStory('', '', '', '', datetime(1987, 10, 15))
        just_now = NewsStory('', '', '', '', now - dt)
        in_a_bit = NewsStory('', '', '', '', now + dt)
        future = NewsStory('', '', '', '', datetime(2087, 10, 15))

        s1 = BeforeTrigger('12 Oct 2016 23:59:59')
        s2 = AfterTrigger('12 Oct 2016 23:59:59')

        self.assertTrue(s1.evaluate(ancient), "BeforeTrigger failed to fire on news from long ago")
        self.assertTrue(s1.evaluate(just_now), "BeforeTrigger failed to fire on news happened right before specified time")

        self.assertFalse(s1.evaluate(in_a_bit), "BeforeTrigger fired to fire on news happened right after specified time")
        self.assertFalse(s1.evaluate(future), "BeforeTrigger fired to fire on news from the future")

        self.assertFalse(s2.evaluate(ancient), "AfterTrigger fired to fire on news from long ago")
        self.assertFalse(s2.evaluate(just_now), "BeforeTrigger fired to fire on news happened right before specified time")

        self.assertTrue(s2.evaluate(in_a_bit), "AfterTrigger failed to fire on news just after specified time")
        self.assertTrue(s2.evaluate(future), "AfterTrigger failed to fire on news from long ago")

    def test4NotTrigger(self):
        n = NotTrigger(self.tt)
        b = NewsStory("guid", "title", "description", "link", datetime.now())

        self.assertFalse(n.evaluate(b), "A NOT trigger applied to 'always true' DID NOT return false")

        y = NotTrigger(self.ft)
        self.assertTrue(y.evaluate(b), "A NOT trigger applied to 'always false' DID NOT return true")

    def test5AndTrigger(self):
        yy = AndTrigger(self.tt, self.tt2)
        yn = AndTrigger(self.tt, self.ft)
        ny = AndTrigger(self.ft, self.tt)
        nn = AndTrigger(self.ft, self.ft2)
        b = NewsStory("guid", "title", "description", "link", datetime.now())

        self.assertTrue(yy.evaluate(b), "AND of 'always true' and 'always true' should be true")
        self.assertFalse(yn.evaluate(b), "AND of 'always true' and 'always false' should be false")
        self.assertFalse(ny.evaluate(b), "AND of 'always false' and 'always true' should be false")
        self.assertFalse(nn.evaluate(b), "AND of 'always false' and 'always false' should be false")

    def test6OrTrigger(self):
        yy = OrTrigger(self.tt, self.tt2)
        yn = OrTrigger(self.tt, self.ft)
        ny = OrTrigger(self.ft, self.tt)
        nn = OrTrigger(self.ft, self.ft2)
        b = NewsStory("guid", "title", "description", "link", datetime.now())

        self.assertTrue(yy.evaluate(b), "OR of 'always true' and 'always true' should be true")
        self.assertTrue(yn.evaluate(b), "OR of 'always true' and 'always false' should be true")
        self.assertTrue(ny.evaluate(b), "OR of 'always false' and 'always true' should be true")
        self.assertFalse(nn.evaluate(b), "OR of 'always false' and 'always false' should be false")

    def test7FilterStories(self):
        tt = TitleTrigger("New York City")
        a = NewsStory('', "asfd New York City asfdasdfasdf", '', '', datetime.now())
        b = NewsStory('', "asdfasfd new york city! asfdasdfasdf", '', '', datetime.now())
        noa = NewsStory('', "something somethingnew york city", '', '', datetime.now())
        nob = NewsStory('', "something something new york cities", '', '', datetime.now())

        st = DescriptionTrigger("New York City")
        a = NewsStory('', '', "asfd New York City asfdasdfasdf", '', datetime.now())
        b = NewsStory('', '', "asdfasfd new york city! asfdasdfasdf", '', datetime.now())
        noa = NewsStory('', '', "something somethingnew york city", '', datetime.now())
        nob = NewsStory('', '', "something something new york cities", '', datetime.now())

        triggers = [tt, st, self.tt, self.ft]
        stories = [a, b, noa, nob]
        filtered_stories = filter_stories(stories, triggers)
        for story in stories:
            self.assertTrue(story in filtered_stories)
        filtered_stories = filter_stories(stories, [self.ft])
        self.assertEqual(len(filtered_stories), 0)

    def test8FilterStories2(self):
        a = NewsStory('', "asfd New York City asfdasdfasdf", '', '', datetime.now())
        b = NewsStory('', "asdfasfd new york city! asfdasdfasdf", '', '', datetime.now())
        noa = NewsStory('', "something somethingnew york city", '', '', datetime.now())
        nob = NewsStory('', "something something new york cities", '', '', datetime.now())

        class MatchTrigger(Trigger):
            def __init__(self, story):
                self.story = story
            def evaluate(self, story):
                return story == self.story
        triggers = [MatchTrigger(a), MatchTrigger(nob)]
        stories = [a, b, noa, nob]
        filtered_stories = filter_stories(stories, triggers)
        self.assertTrue(a in filtered_stories)
        self.assertTrue(nob in filtered_stories)
        self.assertEqual(2, len(filtered_stories))


class ProblemSet5Regression(unittest.TestCase):
    def testVerifiedSslContextHasTrustedCertificates(self):
        context = feedparser._create_verified_ssl_context()
        self.assertGreater(len(context.get_ca_certs()), 0)

    def testTimeTriggersInterpretInputAsEST(self):
        before = BeforeTrigger('12 Oct 2016 23:59:59')
        after = AfterTrigger('12 Oct 2016 23:59:59')

        self.assertEqual(before.time.utcoffset(), timedelta(hours=-5))

        naive_before = NewsStory('', '', '', '', datetime(2016, 10, 12, 23, 59, 58))
        naive_after = NewsStory('', '', '', '', datetime(2016, 10, 13, 0, 0, 0))
        self.assertTrue(before.evaluate(naive_before))
        self.assertTrue(after.evaluate(naive_after))

        same_in_utc = NewsStory(
            '', '', '', '',
            pytz.utc.localize(datetime(2016, 10, 13, 4, 59, 59)),
        )
        self.assertFalse(before.evaluate(same_in_utc))
        self.assertFalse(after.evaluate(same_in_utc))

    def testTranslateHtmlPreservesAmpersandsAndUnicode(self):
        self.assertEqual(
            translate_html('AT&T announces results in München'),
            'AT&T announces results in München',
        )
        self.assertEqual(
            translate_html('Fran&ccedil;ois &amp; Co.'),
            'François & Co.',
        )

    def testProcessParsesRssWithoutTruncatingTitle(self):
        rss = '''
            <rss><channel><item>
              <guid>story-1</guid>
              <title>AT&amp;T opens in München</title>
              <link>https://example.com/story-1</link>
              <description>&lt;b&gt;Café update&lt;/b&gt;</description>
              <pubDate>Sat, 29 Aug 2026 12:00:00 GMT</pubDate>
            </item></channel></rss>
        '''
        story = process(BytesIO(rss.encode('utf-8')))[0]

        self.assertEqual(story.get_title(), 'AT&T opens in München')
        self.assertEqual(story.get_description(), 'Café update')
        self.assertEqual(story.get_link(), 'https://example.com/story-1')
        self.assertEqual(story.get_pubdate().utcoffset(), timedelta(0))

    def testAtomLinkAndIsoTimestamp(self):
        atom = '''
            <feed xmlns="http://www.w3.org/2005/Atom">
              <entry>
                <id>story-2</id>
                <title>Markets &amp; München</title>
                <link href="https://example.com/story-2"/>
                <summary>Summary</summary>
                <updated>2026-08-29T12:00:00Z</updated>
              </entry>
            </feed>
        '''

        parsed_entry = feedparser.parse(BytesIO(atom.encode('utf-8'))).entries[0]
        self.assertEqual(parsed_entry.link, 'https://example.com/story-2')

        story = process(BytesIO(atom.encode('utf-8')))[0]
        self.assertEqual(story.get_link(), 'https://example.com/story-2')
        self.assertEqual(
            story.get_pubdate(),
            pytz.utc.localize(datetime(2026, 8, 29, 12, 0, 0)),
        )

    def testReadTriggerConfigSupportsEveryTriggerType(self):
        config = '''// comment

title,TITLE,Purple Cow
description,DESCRIPTION,Market
before,BEFORE,30 Aug 2026 12:00:00
after,AFTER,28 Aug 2026 12:00:00
not_title,NOT,title
both,AND,title,description
either,OR,title,description
ADD,title,description,before,after,not_title,both,either
'''

        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = Path(temp_dir) / 'triggers.txt'
            config_path.write_text(config, encoding='utf-8')
            triggers = read_trigger_config(config_path)

        story = NewsStory(
            '', 'Purple cow!', 'Market report', '',
            datetime(2026, 8, 29, 12, 0, 0),
        )
        self.assertEqual(
            [trigger.evaluate(story) for trigger in triggers],
            [True, True, True, True, False, True, True],
        )

    def testDebateTriggerFileDefinesThreeHourWindow(self):
        config_path = Path(__file__).with_name('debate_triggers.txt')
        triggers = read_trigger_config(config_path)
        self.assertEqual(len(triggers), 1)

        inside = NewsStory('', '', '', '', datetime(2016, 10, 19, 21, 0, 0))
        too_early = NewsStory('', '', '', '', datetime(2016, 10, 19, 17, 59, 59))
        too_late = NewsStory('', '', '', '', datetime(2016, 10, 20, 0, 0, 1))
        self.assertTrue(triggers[0].evaluate(inside))
        self.assertFalse(triggers[0].evaluate(too_early))
        self.assertFalse(triggers[0].evaluate(too_late))


if __name__ == "__main__":
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(ProblemSet5NewsStory))
    suite.addTests(loader.loadTestsFromTestCase(ProblemSet5))
    suite.addTests(loader.loadTestsFromTestCase(ProblemSet5Regression))
    unittest.TextTestRunner(verbosity=2).run(suite)

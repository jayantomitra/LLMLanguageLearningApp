class LanguageLearning:
      def __init__(self, score, level):
        self.score = score
        self.level = level

      @classmethod
      def setup(cls):
        #install
        !pip install -q google-generativeai
        !pip install -q --upgrade langchain
        !pip install --upgrade --quiet  langchain-google-genai

        #import
        import google.generativeai as genai
        import os
        from google.colab import userdata

        API_KEY = userdata.get('GEMINI_PRO_API_KEY')
        # os.environ['API_KEY'] = API_KEY
        genai.configure(api_key=API_KEY)

        cls.model = genai.GenerativeModel('gemini-pro')
        cls.chat = cls.model.start_chat()

      def update_score(self, ans_value, score):
          if ans_value == 'CORRECT':
              self.score += 10
          elif ans_value == "INCORRECT" and self.score > 0:
              self.score -= 10
          return self.score

      def end_session(self, score):
        print(f"you current score is : {self.score}, Goodbye")

      def voice_output(self, response):
        print(response.text)

      def voice_input(self, prompt):
        response = input(prompt)
        return response

      def askQuestion(self, level):
        self.setup()
        Question = self.chat.send_message(f"Ask only one German to English translation Question at a time, of {level}, do not give the english translation or elaborate about the question")
          # output as voice
        self.voice_output(Question)

        # get input as voice
        user_response = self.voice_input("Enter your Answer: ")

        evaluate = self.chat.send_message(f"check if {user_response} is the correct answer for the question {Question.text}, just respond with CORRECT or INCORRECT and do not elaborate further")
        ans_value = evaluate.text
        print(ans_value)
        self.update_score(ans_value, self.score)
        print(self.score)

      def learn_language(self, level = "Easy"):
        self.askQuestion(self.level)
        while(self.score < 40):
          print("Asking another Question....")
          self.askQuestion(self.level)
          print(f"you current score is : {self.score}")
        else:
          self.end_session(self.score)




# Runner
language_learning_session = LanguageLearning(0, "Easy")
language_learning_session.learn_language("Easy")
print("Current score:", language_learning_session.score)


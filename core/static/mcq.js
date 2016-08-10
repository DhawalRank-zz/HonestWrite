var useranswers = [];
var answered = 0;
var questions = [];
var choices = [];
var answers = [];

// To add more questions, just follow the format below.

questions[0] = "JavaScript is ...";
choices[0] = [];
choices[0][0] = "the same as Java";
choices[0][1] = "kind of like Java";
choices[0][2] = "different than Java";
choices[0][3] = "ther written part of Java";
answers[0] = choices[0][2];

questions[1] = "JavaScript is ...";
choices[1] = [];
choices[1][0] = "subjective";
choices[1][1] = "objective";
choices[1][2] = "evil";
choices[1][3] = "object based";
answers[1] = choices[1][3];

questions[2] = "To comment out a line in JavaScript ...";
choices[2] = [];
choices[2][0] = "Precede it with two forward slashes, i.e. '//'";
choices[2][1] = "Precede it with an asterisk and a forward slash, i.e. '*/'";
choices[2][2] = "Precede it with an asterisk, i.e. '*'";
choices[2][3] = "Precede it with a forward slash and an asterisk, i.e. '/*'";
answers[2] = choices[2][0];

questions[3] = "avaScript can only run on Windows";
choices[3] = [];
choices[3][0] = "True";
choices[3][1] = "False";
answers[3] = choices[3][1];

questions[4] = "5) Semicolons are optional at the end of a JavaScript statement.";
choices[4] = [];
choices[4][0] = "True";
choices[4][1] = "False";
answers[4] = choices[4][0];

questions[5] = "The four basic data types are:";
choices[5] = [];
choices[5][0] = "strings, numbers, BooBoos, and nulls";
choices[5][1] = "strings, text, Booleans, and nulls";
choices[5][2] = "strings, numbers, Booleans, and nulls";
choices[5][3] = "strings, numbers, Booleans, and zeros";
answers[5] = choices[5][2];

function renderQuiz() {
  for(var i=0;i<questions.length;i++) {
    document.writeln('<li type="1"><p class="question">' + questions[i] + ' <span id="result_' + i + '"><img src="/core/static/blank.gif" style="border:0" alt="" /></span></p></li>');
    for(var j=0;j<choices[i].length;j++) {
      document.writeln('<input type="radio" name="answer_' + i + '" value="' + choices[i][j] + '" id="answer_' + i + '_' + j + '" class="question_' + i + '" onclick="submitAnswer(' + i + ', this, \'label_' + i + '_' + j + '\')" /><label id="label_' + i + '_' + j + '" for="answer_' + i + '_' + j + '"> ' + choices[i][j] + '</label><br />');
    }
  }
  document.writeln('<p><input type="submit" class="btn" value="Show Score" onclick="showScore()" /> <input type="submit" class="btn" value="Reset Quiz" onclick="resetQuiz(true)" /></p><p style="display:none"><img src="/core/static/correct.gif" style="border:0" alt="Correct!" /><img src="/core/static/incorrect.gif" style="border:0" alt="Incorrect!" /></p>');
}
function resetQuiz(showConfirm) {
  if(showConfirm)
    if(!confirm("Are you sure you want to reset your answers and start from the beginning?"))
      return false;
  document.location = document.location;
}
function submitAnswer(questionId, obj, labelId) {
  useranswers[questionId] = obj.value;
  console.log(useranswers[questionId]);
  document.getElementById(labelId).style.fontWeight = "bold";
  showResult(questionId);
  answered++;
}
function showResult(questionId) {
  if(answers[questionId] == useranswers[questionId]) {
    document.getElementById('result_' + questionId).innerHTML = '<img src="/core/static/correct.gif" style="border:0" alt="Correct!" />';
  } else {
    document.getElementById('result_' + questionId).innerHTML = '<img src="/core/static/incorrect.gif" style="border:0" alt="Incorrect!" />';
  }
}
function showScore() {
  if(answered < answers.length) {
    alert("You have not correctly answered all of the questions yet!");
    return false;
  }
  var questionCount = answers.length;
  var correct = 0;
  var incorrect = 0;
  for(var i=0;i<questionCount;i++) {
    if(useranswers[i] == answers[i])
      correct++;
    else
      incorrect++;
  }
  if(correct != questions.length)
  {
    alert("You have not correctly answered all of the questions yet!");
  }
  else{
    alert("You have passed the quiz. Your instructor will be updated.");
    resetQuiz(true);
  }
}


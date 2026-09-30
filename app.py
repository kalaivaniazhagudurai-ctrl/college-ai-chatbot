from flask import Flask, render_template, request, jsonify
from datetime import datetime
from college_data import COLLEGE_DATA

app = Flask(__name__)


# -----------------------------------
# HOME PAGE
# -----------------------------------

@app.route("/")
def home():

    college_name = COLLEGE_DATA.get(
        "college_name",
        "College AI Assistant"
    )

    return render_template(
        "index.html",
        college=college_name,
        data=COLLEGE_DATA
    )


# -----------------------------------
# CHAT API
# -----------------------------------

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please type a question."
        })


    message = user_message.lower()


    # -----------------------------------
    # TIME / DATE
    # -----------------------------------

    if "time" in message:

        current_time = datetime.now().strftime(
            "%I:%M %p"
        )

        return jsonify({
            "reply": f"The current time is {current_time}."
        })

    if "timing" in message or "timings" in message:
       return jsonify({
          "reply": "⏰ College timing: 9:15 AM - 4:30 PM"
    })

    if (
    "admission" in message
    or "admissions" in message
    or "apply" in message
    ):
     admission = COLLEGE_DATA.get("admission", {})

     modes = admission.get("mode", [])
     documents = admission.get("documents", [])

     reply = "🎓 Admission Information\n\n"

     reply += "Admission Modes:\n"
     for mode in modes:
        reply += f"• {mode}\n"

     reply += "\nEligibility:\n"
     reply += admission.get("eligibility", "")

     reply += "\n\nRequired Documents:\n"
     for document in documents:
        reply += f"• {document}\n"

     return jsonify({
        "reply": reply
    })  



    # ==============================
# ADMINISTRATION
# ==============================

    if "vice principal" in message:

         administration = COLLEGE_DATA.get("administration", {})

         vice = administration.get("vice_principal", {})

         return jsonify({
           "reply": (
             "👨‍💼 Vice Principal Information\n\n"
             f"Name: {vice.get('name', 'Not available')}\n"
             f"Qualification: {vice.get('qualification', 'Not available')}"
        )
    })


    if "principal" in message and "vice principal" not in message:

           administration = COLLEGE_DATA.get("administration", {})

           principal = administration.get("principal", {})

           return jsonify({
            "reply": (
               "👩‍💼 Principal Information\n\n"
              f"Name: {principal.get('name', 'Not available')}\n"
              f"Qualification: {principal.get('qualification', 'Not available')}"
        )
    })


    if (
    "controller of examination" in message
    or "controller of examinations" in message
    ):

     controller = COLLEGE_DATA.get(
        "administration", {}
     ).get("controller_of_examinations", {})

     return jsonify({
        "reply": (
            "📋 Controller of Examinations\n\n"
            f"Name: {controller.get('name', '')}"
        )
    })
    # ==============================
# FACULTY INFORMATION
# ==============================

    if (
    "faculty" in message
    or "faculties" in message
    or "faculty details" in message
    ):

         faculty_data = COLLEGE_DATA.get("faculty", {})

         reply = "👨‍🏫 Faculty Information\n\n"

         if not faculty_data:
          return jsonify({
            "reply": "Faculty information is not available."
          })

         for department, details in faculty_data.items():

          reply += f"📚 {department.upper()}\n"

          hod = details.get("hod", "")

          if hod:
            reply += f"HOD: {hod}\n"

          faculty_list = details.get("faculty", [])

          for name in faculty_list:
            reply += f"• {name}\n"

          reply += "\n"

          return jsonify({
        "reply": reply
         })


# ==============================
# VICE PRINCIPAL
# ==============================

    if "vice principal" in message:

         administration = COLLEGE_DATA.get(
        "administration",
        {}
       )

         vice = administration.get(
        "vice_principal",
        {}
         )

         return jsonify({
        "reply": (
            "👨‍💼 Vice Principal Information\n\n"
            f"Name: {vice.get('name', '')}\n"
            f"Qualification: {vice.get('qualification', '')}"
          )
         })


# ==============================
# PRINCIPAL
# ==============================

    if (
       "principal" in message
      and "vice principal" not in message
      ):

       administration = COLLEGE_DATA.get(
        "administration",
        {}
      )

       principal = administration.get(
        "principal",
        {}
      )

       return jsonify({
        "reply": (
            "👩‍💼 Principal Information\n\n"
            f"Name: {principal.get('name', '')}\n"
            f"Qualification: {principal.get('qualification', '')}"
        )
     })


# ==============================
# CONTROLLER OF EXAMINATIONS
# ==============================

    if (
     "controller of examination" in message
     or "controller of examinations" in message
):

      administration = COLLEGE_DATA.get(
        "administration",
        {}
     )

      controller = administration.get(
        "controller_of_examinations",
        {}
      )

      return jsonify({
        "reply": (
            "📋 Controller of Examinations\n\n"
            f"Name: {controller.get('name', '')}"
        )
    })



    if "hod" in message or "head of department" in message:

     hods = COLLEGE_DATA.get("hods", {})

     if "civil" in message:
        hod = hods.get("civil", {})
        reply = (
            f"👨‍🏫 Civil Engineering HOD\n\n"
            f"Name: {hod.get('name', '')}\n"
            f"Qualification: {hod.get('qualification', '')}\n"
            f"Experience: {hod.get('experience', '')}"
        )

     elif "cse" in message or "computer science" in message:
        hod = hods.get("cse", {})
        reply = (
            f"👩‍🏫 CSE HOD\n\n"
            f"Name: {hod.get('name', '')}\n"
            f"Qualification: {hod.get('qualification', '')}\n"
            f"Experience: {hod.get('experience', '')}"
        )

     elif "ece" in message or "electronics" in message:
        hod = hods.get("ece", {})
        reply = (
            f"👩‍🏫 ECE HOD\n\n"
            f"Name: {hod.get('name', '')}\n"
            f"Qualification: {hod.get('qualification', '')}\n"
            f"Experience: {hod.get('experience', '')}"
        )

     elif "eee" in message or "electrical" in message:
        hod = hods.get("eee", {})
        reply = (
            f"👨‍🏫 EEE HOD\n\n"
            f"Name: {hod.get('name', '')}\n"
            f"Qualification: {hod.get('qualification', '')}\n"
            f"Experience: {hod.get('experience', '')}"
        )

     elif "mechanical" in message:
        hod = hods.get("mechanical", {})
        reply = (
            f"👨‍🏫 Mechanical Engineering HOD\n\n"
            f"Name: {hod.get('name', '')}\n"
            f"Qualification: {hod.get('qualification', '')}\n"
            f"Experience: {hod.get('experience', '')}"
        )

     else:
        reply = (
            "👨‍🏫 HOD Information\n\n"
            "I can provide HOD details for:\n"
            "• Civil Engineering\n"
            "• Computer Science and Engineering\n"
            "• Electronics and Communication Engineering\n"
            "• Electrical and Electronics Engineering\n"
            "• Mechanical Engineering"
        )

     return jsonify({
        "reply": reply
    })

    if (
       "placement" in message
       or "placements" in message
       or "job" in message
       or "jobs" in message
):
       placement = COLLEGE_DATA.get("placement", {})

       reply = (
         "💼 Placement Information\n\n"
         + placement.get(
            "description",
            "Placement information is not available."
           )
          )

       return jsonify({
        "reply": reply
    })

    if "principal" in message:
        principal = COLLEGE_DATA.get("faculty", {}).get(
            "principal", {}
        )

        reply = (
            "👩‍💼 Principal Details\n\n"
            f"Name: {principal.get('name', '')}\n"
            f"Position: {principal.get('position', '')}\n\n"
            "🎓 Qualifications:\n"
        )

        for qualification in principal.get("qualification", []):
            reply += f"• {qualification}\n"

        return jsonify({
            "reply": reply
        })
    if (
        "cse hod" in message
        or "hod of cse" in message
        or "computer science hod" in message
    ):
        cse = COLLEGE_DATA.get("faculty", {}).get("cse", {})
        hod = cse.get(
            "hod",
            "CSE HOD information is not available."
        )

        return jsonify({
            "reply": f"👨‍🏫 CSE HOD: {hod}"
        })


    if (
        "cse faculty" in message
        or "cse staffs" in message
        or "cse staff" in message
        or "computer science faculty" in message
    ):
        cse = COLLEGE_DATA.get("faculty", {}).get("cse", {})
        faculty = cse.get("faculty", [])

        reply = "👨‍🏫 CSE Faculty:\n\n"

        for person in faculty:
            reply += f"• {person}\n"

        return jsonify({
            "reply": reply
        })

    if "date" in message or "today" in message:

        current_date = datetime.now().strftime(
            "%d %B %Y"
        )

        return jsonify({
            "reply": f"Today's date is {current_date}."
        })


    # -----------------------------------
    # COLLEGE NAME
    # -----------------------------------

    if "college name" in message or "college" == message:

        return jsonify({
            "reply": (
                f"The college name is "
                f"{COLLEGE_DATA.get('college_name', '')}."
            )
        })


    # -----------------------------------
    # COURSES
    # -----------------------------------

    if (
        "course" in message
        or "courses" in message
        or "department" in message
        or "departments" in message
    ):

        courses = COLLEGE_DATA.get(
            "courses",
            []
        )

        if courses:

            reply = "Here are the courses offered:\n\n"

            for course in courses:

                if isinstance(course, dict):

                    reply += (
                        f"📘 {course.get('name', '')}\n"
                    )

                else:

                    reply += f"📘 {course}\n"

            return jsonify({
                "reply": reply
            })
    # ==============================
# COLLEGE INTAKE
# ==============================

    if (
        "intake" in message
        or "seat" in message
        or "seats" in message
        or "how many seats" in message
):

        intake_data = COLLEGE_DATA.get("intake", {})

        ug = intake_data.get("undergraduate", [])
        pg = intake_data.get("postgraduate", [])

        reply = "🎓 College Intake Information\n\n"

        reply += "📚 Undergraduate:\n\n"

        for item in ug:
         reply += f"• {item['course']}: {item['seats']} seats\n"

         reply += "\n🎓 Postgraduate:\n\n" 

         for item in pg:
           reply += f"• {item['course']}: {item['seats']} seats\n"

         return jsonify({
           "reply": reply
    })

        # ==============================
# FEES
# ==============================

    if (
      "fee" in message
      or  "fees" in message
      or "tuition fee" in message
      or "college fee" in message
):

      fees = COLLEGE_DATA.get("fees", {})

      return jsonify({
          "reply": (
              "💰 Fee Information\n\n"
              f"{fees.get('status', '')}\n\n"
              f"{fees.get('official_note', '')}\n\n"
              "For the latest 2026-27 fee details, "
              "please contact the KCE admission office."
        )
    })


    # ==============================
# SCHOLARSHIP
# ==============================

    if (
      "scholarship" in message
      or "scholarships" in message
      or "fee waiver" in message
):

       scholarship = COLLEGE_DATA.get("scholarship", {})

       details = scholarship.get("details", [])

       reply = "🎓 Scholarship Information\n\n"

       for item in details:
          reply += f"• {item}\n"

          reply += (
           "\n\nNote:\n"
          + scholarship.get("note", "")
    )

          return jsonify({
           "reply": reply
    })

         # ==============================
# HOSTEL
# ==============================

    if (
    "hostel" in message
    or "hostels" in message
    or "hostel facility" in message
):

       hostel = COLLEGE_DATA.get("hostel", {})

       details = hostel.get("details", [])

       reply = "🏠 Hostel Information\n\n"

       for item in details:
        reply += f"• {item}\n"

       reply += (
        "\n\nNote:\n"
        + hostel.get("note", "")
    )

       return jsonify({
        "reply": reply
    })


    # ==============================
# TRANSPORT
# ==============================

    if (
    "transport" in message
    or "transportation" in message
    or "college bus" in message
    or "bus facility" in message
):

       transport = COLLEGE_DATA.get("transport", {})

       details = transport.get("details", [])

       reply = "🚌 Transport Information\n\n"

       for item in details:
        reply += f"• {item}\n"

       reply += (
        "\n\nNote:\n"
        + transport.get("note", "")
    )

       return jsonify({
        "reply": reply
    })


    # ==============================
# LIBRARY
# ==============================

    if (
    "library" in message
    or "libraries" in message
    or "library facility" in message
):

       library = COLLEGE_DATA.get("library", {})

       details = library.get("details", [])

       reply = "📚 Library Information\n\n"

       for item in details:
        reply += f"• {item}\n"

       reply += (
        "\n\nNote:\n"
        + library.get("note", "")
    )

       return jsonify({
        "reply": reply
    })


    # ==============================
# CLUBS & STUDENT ACTIVITIES
# ==============================

    if (
    "club" in message
    or "clubs" in message
    or "student activities" in message
    or "activities" in message
):

       clubs = COLLEGE_DATA.get("clubs", {})

       details = clubs.get("details", [])

       reply = "🏆 Clubs & Student Activities\n\n"

       for item in details:
        reply += f"• {item}\n"

       reply += (
        "\n\n"
        + clubs.get("note", "")
    )

       return jsonify({
        "reply": reply
    })

    # ==============================
# NCC & NSS
# ==============================

    if (
    "ncc" in message
    or "nss" in message
    or "national cadet corps" in message
    or "national service scheme" in message
):

       ncc_nss = COLLEGE_DATA.get("ncc_nss", {})

       details = ncc_nss.get("details", [])

       reply = "🪖 NCC & NSS Information\n\n"

       for item in details:
        reply += f"• {item}\n"

       reply += (
        "\n\n"
        + ncc_nss.get("note", "")
    )

       return jsonify({
        "reply": reply
    })


         # ==============================
# CAMPUS & INFRASTRUCTURE
# ==============================

    if (
    "campus" in message
    or "infrastructure" in message
    or "campus facilities" in message
):

      campus = COLLEGE_DATA.get("campus", {})

      details = campus.get("details", [])

      reply = "🏫 Campus & Infrastructure\n\n"

      for item in details:
        reply += f"• {item}\n"

      reply += (
        "\n\n"
        + campus.get("note", "")
    )

      return jsonify({
        "reply": reply
    })

    # -----------------------------------
    # FACILITIES
    # -----------------------------------

    if (
        "facility" in message
        or "facilities" in message
        or "campus" in message
        or "library" in message
        or "hostel" in message
        or "transport" in message
    ):

        facilities = COLLEGE_DATA.get(
            "facilities",
            []
        )

        if facilities:

            reply = "College facilities include:\n\n"

            for facility in facilities:

                reply += f"🏫 {facility}\n"

            return jsonify({
                "reply": reply
            })


    # -----------------------------------
    # ABOUT COLLEGE
    # -----------------------------------

    if (
        "about" in message
        or "history" in message
        or "tell me about" in message
    ):

        about = COLLEGE_DATA.get(
            "about",
            "College information is available."
        )

        return jsonify({
            "reply": about
        })


    # -----------------------------------
    # WEBSITE
    # -----------------------------------

    if (
        "website" in message
        or "web site" in message
        or "official site" in message
    ):

        website = COLLEGE_DATA.get(
            "website",
            ""
        )

        if website:

            return jsonify({
                "reply": (
                    f"You can visit the official "
                    f"college website here:\n{website}"
                )
            })


    # -----------------------------------
    # CONTACT
    # -----------------------------------

    location_words = [
    "location",
    "locaton",
    "locashun",
    "address",
    "college enga",
    "clg enga",
    "enga iruku",
    "enga irukku",
    "where is college",
    "where is the college"
]

    if any(word in message for word in location_words):
    address = COLLEGE_DATA.get("address", "")

    return jsonify({
        "reply": f"📍 College Location: {address}"
    })


    # -----------------------------------
    # GREETING
    # -----------------------------------

    if any(word in message for word in [
        "hi",
        "hello",
        "hey",
        "vanakkam"
    ]):

        return jsonify({
            "reply": (
                "Hello! 👋\n\n"
                "I'm your College AI Assistant. "
                "You can ask me about courses, "
                "admission, facilities, hostel, "
                "transport, placement, contact "
                "details and more."
            )
        })


    # -----------------------------------
    # DEFAULT RESPONSE
    # -----------------------------------

    return jsonify({
        "reply": (
            "I'm your College AI Assistant 🤖\n\n"
            "I can currently help you with:\n\n"
            "📚 Courses\n"
            "🎓 Admission\n"
            "🏫 Campus & Facilities\n"
            "🚌 Transport\n"
            "🏠 Hostel\n"
            "💼 Placement\n"
            "🌐 College Website\n"
            "📞 Contact Details\n"
            "🕐 Date & Time\n\n"
            "Try asking one of these questions."
        )
    })


# -----------------------------------
# RUN APPLICATION
# -----------------------------------
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
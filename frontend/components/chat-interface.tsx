"use client"

import React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Building2, MapPin, DollarSign } from "lucide-react"

interface Message {
  id: string
  content: string
  isUser: boolean
  timestamp: Date
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your AI deal sourcing agent. I can help you find investment opportunities in real estate and business deals. What type of opportunities are you looking for?",
      isUser: false,
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isUser: true,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const currentInputValue = inputValue
    setInputValue("")
    setIsLoading(true)

    try {
      // Call the backend API with better error handling
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentInputValue,
          conversation_history: messages
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || `HTTP error! status: ${response.status}`)
      }

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: data.response || "I'm processing your request through the Agent Engine...",
        isUser: false,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, aiResponse])
    } catch (error) {
      console.error('Error calling backend:', error)

      let errorMessage = "I'm having trouble connecting to the investment analysis system. "

      if (error instanceof Error) {
        if (error.message.includes('Agent Engine not configured')) {
          errorMessage += "🚀 The Agent Engine is currently being deployed to Vertex AI. Please try again in a few minutes!"
        } else {
          errorMessage += "Please try again later."
        }
      }

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        content: `⚠️ ${errorMessage}`,
        isUser: false,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, aiResponse])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Hero Background with Building Image */}
      <div className="absolute inset-0">
        {/* Fallback gradient background */}
        <div className="absolute inset-0 bg-gradient-to-br from-slate-100 via-blue-50 to-indigo-100" />

        {/* Main background image - more visible */}
        <div
          className="absolute inset-0 bg-cover bg-center opacity-70"
          style={{
            backgroundImage: `url('/modern-city-skyline-slate-professional.jpg'),
              linear-gradient(135deg, #1e293b 0%, #475569 25%, #64748b 50%, #94a3b8 75%, #cbd5e1 100%)`
          }}
        />

        {/* Geometric pattern overlay for modern look */}
        <div
          className="absolute inset-0 opacity-20"
          style={{
            backgroundImage: `
              linear-gradient(45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%),
              linear-gradient(-45deg, transparent 40%, rgba(255,255,255,0.1) 50%, transparent 60%)
            `,
            backgroundSize: '60px 60px'
          }}
        />

        {/* Gradient overlay for depth and color */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/30 via-slate-800/20 to-indigo-900/30" />

        {/* Bottom fade to ensure readability */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-50/90 via-slate-50/40 to-slate-50/5" />

        {/* Top vignette */}
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/10 via-transparent to-transparent" />
      </div>

      {/* Content */}
      <div className="relative z-10 flex flex-col min-h-screen">
        {/* Header */}
        <div className="text-center pt-16 pb-8 px-4 animate-fade-in">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-xl shadow-lg transition-all duration-500 hover:scale-110 hover:rotate-3">
              <Building2 className="h-12 w-12 text-slate-800 drop-shadow-lg" />
            </div>
            <h1 className="text-6xl font-bold text-balance text-slate-800 drop-shadow-lg">
              HW Deal<span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 animate-pulse">Sourcing</span>
            </h1>
          </div>
          <p className="text-xl text-slate-700 max-w-2xl mx-auto text-balance font-medium drop-shadow-sm">
            Your intelligent deal sourcing agent. Find the perfect investment opportunities with AI-powered search.
          </p>
        </div>

        {/* Chat Container */}
        <div className="flex-1 max-w-4xl mx-auto w-full px-4 pb-8">
          <Card className="h-[500px] flex flex-col bg-white/85 backdrop-blur-md border-white/20 shadow-2xl">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-3 shadow-md ${
                      message.isUser ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white" : "bg-white/90 backdrop-blur-sm text-slate-700 border border-slate-200/50"
                    }`}
                  >
                    <p className="text-sm leading-relaxed">{message.content}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white/90 backdrop-blur-sm text-slate-700 rounded-lg px-4 py-3 shadow-md border border-slate-200/50">
                    <div className="flex items-center gap-2">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                        <div
                          className="w-2 h-2 bg-current rounded-full animate-bounce"
                          style={{ animationDelay: "0.1s" }}
                        />
                        <div
                          className="w-2 h-2 bg-current rounded-full animate-bounce"
                          style={{ animationDelay: "0.2s" }}
                        />
                      </div>
                      <span className="text-sm">Searching opportunities...</span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Input Area */}
            <div className="border-t border-slate-200/30 bg-white/50 backdrop-blur-sm p-4">
              <div className="flex gap-2">
                <Input
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me about real estate, M&A deals, investment opportunities..."
                  className="flex-1 bg-white/70 border-slate-300/50 focus:bg-white transition-colors"
                  disabled={isLoading}
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  className="px-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="max-w-4xl mx-auto w-full px-4 pb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              variant="outline"
              className="h-auto p-4 bg-white/80 backdrop-blur-md border-white/30 hover:bg-white/95 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
              onClick={() => setInputValue("Find multifamily properties under $5M in Denver")}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-blue-100 to-indigo-100 rounded-lg">
                  <Building2 className="h-5 w-5 text-blue-600" />
                </div>
                <div className="text-left">
                  <p className="font-semibold text-slate-800">Real Estate Deals</p>
                  <p className="text-sm text-slate-600">Multifamily Properties</p>
                </div>
              </div>
            </Button>

            <Button
              variant="outline"
              className="h-auto p-4 bg-white/80 backdrop-blur-md border-white/30 hover:bg-white/95 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
              onClick={() => setInputValue("Search for M&A opportunities in the technology sector")}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-green-100 to-emerald-100 rounded-lg">
                  <DollarSign className="h-5 w-5 text-green-600" />
                </div>
                <div className="text-left">
                  <p className="font-semibold text-slate-800">M&A Opportunities</p>
                  <p className="text-sm text-slate-600">Tech Sector</p>
                </div>
              </div>
            </Button>

            <Button
              variant="outline"
              className="h-auto p-4 bg-white/80 backdrop-blur-md border-white/30 hover:bg-white/95 shadow-lg transition-all duration-300 hover:shadow-xl hover:scale-105"
              onClick={() => setInputValue("Generate a comprehensive investment report on all opportunities")}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-purple-100 to-violet-100 rounded-lg">
                  <MapPin className="h-5 w-5 text-purple-600" />
                </div>
                <div className="text-left">
                  <p className="font-semibold text-slate-800">Investment Report</p>
                  <p className="text-sm text-slate-600">Full Analysis</p>
                </div>
              </div>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}